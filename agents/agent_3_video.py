"""
AGENT 3: VIDEO PRODUCER 🎬
MoviePy Edition - Compilación de videos con ElevenLabs + Stock Footage

Responsabilidad:
- Script → Voiceover (ElevenLabs TTS)
- Obtener background (Pexels gratis)
- Compilar video (MoviePy)
- Agregar subtítulos dinámicos
- Output: MP4 vertical (1080x1920)

Entrada: {trend_title, script, duration_seconds, platform}
Salida: {video_path, duration, filesize_mb, generated_at}

COSTOS: €0-5/mes (ElevenLabs free tier + Pexels gratis)
"""

import asyncio
import logging
import json
import os
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
import requests
import sys

try:
    from moviepy.editor import (
        VideoFileClip, AudioFileClip, CompositeAudioClip,
        TextClip, CompositeVideoClip, ImageClip
    )
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    logging.warning("⚠️ MoviePy no instalado. Run: pip install moviepy")

try:
    from elevenlabs.client import ElevenLabs
    from elevenlabs import stream
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    logging.warning("⚠️ ElevenLabs SDK no instalado. Run: pip install elevenlabs")

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.base import BaseAgent
from config.settings import settings

logger = logging.getLogger(__name__)


class VideoProducer(BaseAgent):
    """Produce videos from scripts using MoviePy + ElevenLabs"""

    def __init__(self, region: str = "es"):
        super().__init__(name="VideoProducer", region=region)
        self.elevenlabs_key = settings.ELEVENLABS_API_KEY
        self.pexels_key = settings.PEXELS_API_KEY

        # Create output directory
        self.output_dir = project_root / "output" / "videos"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"📁 Video output dir: {self.output_dir}")

    async def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate video from script.

        Input:
        {
            "trend_title": "OpenAI lanza GPT-5",
            "script": "Hook: ... Loop: ... CTA: ...",
            "duration_seconds": 60,
            "platform": "tiktok"
        }

        Output:
        {
            "video_path": "/path/to/video.mp4",
            "duration": 60,
            "file_size_mb": 15.5,
            "generated_at": "2026-05-11T19:30:00",
            "cost_estimate": 0.05
        }
        """
        try:
            if not MOVIEPY_AVAILABLE:
                raise Exception("MoviePy no disponible. Install: pip install moviepy")

            trend_title = input_data.get("trend_title", "Trending")
            script = input_data.get("script", "")
            duration = input_data.get("duration_seconds", 60)
            platform = input_data.get("platform", "tiktok")

            self.logger.info(f"🎬 Produciendo video: {trend_title}")

            # Step 1: Generate voiceover
            self.logger.info("🔊 Generando voiceover...")
            voiceover_path = await self._generate_voiceover(script, trend_title)

            # Step 2: Get background footage
            self.logger.info("🎞️ Obteniendo background...")
            bg_path = await self._get_background(trend_title)

            # Step 3: Compile video
            self.logger.info("✂️ Compilando video...")
            video_path = await self._compile_video(
                bg_path=bg_path,
                voiceover_path=voiceover_path,
                script=script,
                duration=duration,
                platform=platform
            )

            # Get file size
            file_size_mb = os.path.getsize(video_path) / (1024 * 1024)

            self.logger.info(f"✅ Video listo: {Path(video_path).name} ({file_size_mb:.1f}MB)")

            return {
                "status": "success",
                "result": {
                    "video_path": str(video_path),
                    "duration": duration,
                    "file_size_mb": round(file_size_mb, 1),
                    "platform": platform,
                    "generated_at": datetime.now().isoformat(),
                    "cost_estimate": 0.05 if self.elevenlabs_key else 0.0
                }
            }

        except Exception as e:
            self.logger.error(f"❌ VideoProducer error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def _generate_voiceover(self, script: str, trend_title: str) -> str:
        """Generate voiceover with ElevenLabs API"""
        try:
            if not self.elevenlabs_key:
                self.logger.warning("⚠️ ELEVENLABS_API_KEY no configurado")
                return await self._generate_silence()

            # Extract text (remove timestamps)
            text_clean = script.replace("[", "").replace("]", "")[:500]

            self.logger.info(f"📝 Voiceover text ({len(text_clean)} chars)")

            # Use ElevenLabs REST API (más confiable que SDK)
            url = "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM"
            headers = {
                "xi-api-key": self.elevenlabs_key,
                "Content-Type": "application/json"
            }
            data = {
                "text": text_clean,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.75
                }
            }

            response = requests.post(url, json=data, headers=headers, timeout=30)

            if response.status_code == 200:
                voice_path = self.output_dir / f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                with open(voice_path, 'wb') as f:
                    f.write(response.content)
                self.logger.info(f"✅ Voiceover: {voice_path.name}")
                return str(voice_path)
            else:
                self.logger.warning(f"⚠️ ElevenLabs {response.status_code}")
                return await self._generate_silence()

        except Exception as e:
            self.logger.warning(f"⚠️ Voiceover error: {str(e)}")
            return await self._generate_silence()

    async def _generate_silence(self) -> str:
        """Fallback: create silence audio"""
        try:
            import numpy as np
            from scipy.io import wavfile

            sample_rate = 44100
            silence = np.zeros(sample_rate * 30)  # 30s silencio

            audio_path = self.output_dir / f"silence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
            wavfile.write(audio_path, sample_rate, silence.astype(np.int16))

            self.logger.info(f"⚠️ Silence fallback: {audio_path.name}")
            return str(audio_path)
        except:
            raise Exception("Cannot generate silence audio")

    async def _get_background(self, trend_title: str) -> str:
        """Get background video from Pexels (free)"""
        try:
            if not self.pexels_key:
                self.logger.warning("⚠️ PEXELS_API_KEY no configurado. Using color fallback...")
                return await self._create_color_background()

            search = trend_title.replace(" ", "+")[:50]
            url = f"https://api.pexels.com/videos/search?query={search}&per_page=1"
            headers = {"Authorization": self.pexels_key}

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                if data.get("videos"):
                    video_url = data["videos"][0]["video_files"][0]["link"]
                    bg_path = self.output_dir / f"bg_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

                    self.logger.info(f"📥 Descargando Pexels video...")
                    video_data = requests.get(video_url, timeout=30).content

                    with open(bg_path, 'wb') as f:
                        f.write(video_data)

                    self.logger.info(f"✅ Background: {bg_path.name}")
                    return str(bg_path)

            return await self._create_color_background()

        except Exception as e:
            self.logger.warning(f"⚠️ Pexels error: {str(e)}")
            return await self._create_color_background()

    async def _create_color_background(self) -> str:
        """Fallback: create gradient background video"""
        try:
            import numpy as np
            from moviepy.video.io.ImageSequenceClip import ImageSequenceClip

            self.logger.info("🎨 Creando fondo de color...")

            width, height = 1080, 1920
            fps = 30
            duration = 60
            frames = []

            # Gradient púrpura → azul oscuro
            for frame_idx in range(duration * fps):
                frame = np.zeros((height, width, 3), dtype=np.uint8)
                for y in range(height):
                    ratio = y / height
                    r = int(102 * (1 - ratio))
                    g = int(51 * ratio)
                    b = int(204 * (1 - ratio) + 102 * ratio)
                    frame[y, :] = [r, g, b]
                frames.append(frame)

            bg_path = self.output_dir / f"bg_color_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            clip = ImageSequenceClip(frames, fps=fps)
            clip.write_videofile(str(bg_path), verbose=False, logger=None)
            clip.close()

            self.logger.info(f"✅ Color background: {bg_path.name}")
            return str(bg_path)

        except Exception as e:
            self.logger.error(f"❌ Color background failed: {str(e)}")
            raise

    async def _compile_video(
        self,
        bg_path: str,
        voiceover_path: str,
        script: str,
        duration: int,
        platform: str
    ) -> str:
        """Compile final video with MoviePy"""
        try:
            # Load clips
            bg = VideoFileClip(bg_path)
            voice = AudioFileClip(voiceover_path)

            # Resize to vertical (1080x1920)
            w, h = bg.size
            if w > h:  # Horizontal video
                bg = bg.crop(x1=w, y1=max(0, (h-int(w*16/9))//2), y2=min(h, (h+int(w*16/9))//2))
            bg = bg.resize((1080, 1920))

            # Match duration to voiceover
            target_dur = min(duration, voice.duration + 2)

            if bg.duration < target_dur:
                num_loops = int(target_dur / bg.duration) + 1
                bg = bg.loop(n=num_loops).subclipped(0, target_dur)
            else:
                bg = bg.subclipped(0, target_dur)

            # Create subtitles
            subtitle_clips = self._create_subtitles(script, target_dur)

            # Compose
            final_clips = [bg] + subtitle_clips
            final = CompositeVideoClip(final_clips)
            final = final.set_audio(voice)

            # Write
            output_path = self.output_dir / f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"

            self.logger.info(f"🎥 Escribiendo {output_path.name}...")
            final.write_videofile(
                str(output_path),
                fps=30,
                codec="libx264",
                audio_codec="aac",
                verbose=False,
                logger=None
            )

            bg.close()
            voice.close()
            final.close()

            return str(output_path)

        except Exception as e:
            self.logger.error(f"❌ Compilation error: {str(e)}")
            raise

    def _create_subtitles(self, script: str, duration: float) -> list:
        """Create dynamic subtitle clips"""
        clips = []
        lines = [l.strip() for l in script.split("\n") if l.strip()]

        if not lines:
            return clips

        time_per_line = duration / len(lines) if lines else duration

        for idx, line in enumerate(lines[:10]):  # Max 10 subtitles
            start = idx * time_per_line
            end = (idx + 1) * time_per_line
            text = line.replace("[", "").replace("]", "")

            try:
                txt = (
                    TextClip(
                        text,
                        fontsize=48,
                        color="white",
                        font="Arial-Bold",
                        stroke_color="black",
                        stroke_width=3,
                        method="caption",
                        size=(900, None)
                    )
                    .set_start(start)
                    .set_end(end)
                    .set_position(("center", 0.7), relative=True)
                )
                clips.append(txt)
            except:
                continue

        return clips


async def test_video_producer():
    """Test del agente"""

    agent = VideoProducer(region="es")
    result = await agent.execute({
        "script": "[Voiceover] Test script",
        "trend_id": "trend_001",
        "platform": "tiktok"
    })

    print("\n" + "=" * 60)
    print("🎬 VIDEO PRODUCER TEST RESULT")
    print("=" * 60)
    print(f"Status: {result['status']}")
    print(f"Video URL: {result['result']['video_url']}")
    print(f"Duration: {result['result']['duration']}s")
    print(f"Size: {result['result']['filesize_mb']}MB")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_video_producer())
