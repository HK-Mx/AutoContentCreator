"""
AGENT 4: PUBLISHER 📱
Multi-platform Video Distribution (TikTok + Instagram + YouTube)

Responsabilidad:
- Publicar video en TikTok API v2
- Publicar en Instagram Graph API
- Publicar en YouTube Data API v3
- Trackear URLs de publicación
- Retornar metadata de cada plataforma

Entrada: {video_path, title, description, tags, platform[]}
Salida: {status, results: [{platform, video_url, upload_status, published_at}]}

COSTOS: €0/mes (APIs nativas, sin upload fees)
"""

import asyncio
import logging
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime
import requests
import sys

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    logging.warning("⚠️ google-auth-oauthlib no instalado. Run: pip install google-auth-oauthlib")

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from agents.base import BaseAgent
from config.settings import settings

logger = logging.getLogger(__name__)


class Publisher(BaseAgent):
    """Publish videos to TikTok, Instagram, YouTube"""

    def __init__(self, region: str = "es"):
        super().__init__(name="Publisher", region=region)

        # API Keys
        self.tiktok_access_token = settings.TIKTOK_ACCESS_TOKEN
        self.instagram_access_token = settings.INSTAGRAM_ACCESS_TOKEN
        self.youtube_access_token = settings.YOUTUBE_ACCESS_TOKEN
        self.youtube_client_secret = settings.YOUTUBE_CLIENT_SECRET_PATH

        # Create output directory for metadata
        self.output_dir = project_root / "output" / "publications"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"📁 Publications output dir: {self.output_dir}")

    async def _execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Publish video to multiple platforms.

        Input:
        {
            "video_path": "/path/to/video.mp4",
            "title": "OpenAI lanza GPT-5",
            "description": "Mira cómo OpenAI revoluciona...",
            "tags": ["AI", "tech", "news"],
            "platforms": ["tiktok", "instagram", "youtube"],
            "thumbnail_path": "/path/to/thumbnail.jpg"  # Optional
        }

        Output:
        {
            "status": "success",
            "results": [
                {
                    "platform": "tiktok",
                    "video_url": "https://www.tiktok.com/@user/video/123456",
                    "video_id": "123456",
                    "upload_status": "published",
                    "published_at": "2026-05-11T19:30:00"
                },
                ...
            ]
        }
        """
        try:
            video_path = input_data.get("video_path", "")
            title = input_data.get("title", "Untitled")
            description = input_data.get("description", "")
            tags = input_data.get("tags", [])
            platforms = input_data.get("platforms", ["tiktok", "instagram", "youtube"])
            thumbnail_path = input_data.get("thumbnail_path")

            if not os.path.exists(video_path):
                raise Exception(f"Video not found: {video_path}")

            self.logger.info(f"📤 Publicando en {len(platforms)} plataformas: {platforms}")

            results = []

            # Publish to each platform
            if "tiktok" in platforms:
                self.logger.info("📤 Publicando en TikTok...")
                tiktok_result = await self._publish_tiktok(video_path, title, description, tags)
                results.append(tiktok_result)

            if "instagram" in platforms:
                self.logger.info("📤 Publicando en Instagram...")
                instagram_result = await self._publish_instagram(video_path, title, description)
                results.append(instagram_result)

            if "youtube" in platforms:
                self.logger.info("📤 Publicando en YouTube...")
                youtube_result = await self._publish_youtube(
                    video_path, title, description, tags, thumbnail_path
                )
                results.append(youtube_result)

            # Save publication record
            record_path = self.output_dir / f"publication_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(record_path, 'w', encoding='utf-8') as f:
                json.dump({
                    "title": title,
                    "published_at": datetime.now().isoformat(),
                    "platforms": len(results),
                    "results": results
                }, f, indent=2, ensure_ascii=False)

            self.logger.info(f"✅ Publicación completada: {len(results)}/{len(platforms)} plataformas")

            return {
                "status": "success",
                "result": {
                    "title": title,
                    "platforms_published": len(results),
                    "results": results,
                    "record_path": str(record_path),
                    "published_at": datetime.now().isoformat()
                }
            }

        except Exception as e:
            self.logger.error(f"❌ Publisher error: {str(e)}")
            return {
                "status": "error",
                "error": str(e)
            }

    async def _publish_tiktok(self, video_path: str, title: str, description: str, tags: List[str]) -> Dict[str, Any]:
        """Publish to TikTok via TikTok API v2"""
        try:
            if not self.tiktok_access_token:
                self.logger.warning("⚠️ TIKTOK_ACCESS_TOKEN no configurado")
                return {
                    "platform": "tiktok",
                    "upload_status": "skipped",
                    "reason": "API token not configured"
                }

            # TikTok API endpoint for video upload
            url = "https://open.tiktokapis.com/v1/video/upload/"

            headers = {
                "Authorization": f"Bearer {self.tiktok_access_token}",
                "Content-Type": "application/octet-stream"
            }

            # Upload video file
            with open(video_path, 'rb') as f:
                response = requests.post(
                    url,
                    headers=headers,
                    data=f,
                    timeout=300,
                    params={
                        "video_title": title[:150],
                        "description": description[:2200],
                        "access_token": self.tiktok_access_token
                    }
                )

            if response.status_code in [200, 201]:
                data = response.json()
                video_id = data.get("data", {}).get("video_id", "unknown")

                self.logger.info(f"✅ TikTok published: {video_id}")
                return {
                    "platform": "tiktok",
                    "video_id": video_id,
                    "video_url": f"https://www.tiktok.com/@yourusername/video/{video_id}",
                    "upload_status": "published",
                    "published_at": datetime.now().isoformat()
                }
            else:
                self.logger.warning(f"⚠️ TikTok API error: {response.status_code} - {response.text}")
                return {
                    "platform": "tiktok",
                    "upload_status": "failed",
                    "error": response.text[:200]
                }

        except Exception as e:
            self.logger.error(f"❌ TikTok publish error: {str(e)}")
            return {
                "platform": "tiktok",
                "upload_status": "error",
                "error": str(e)
            }

    async def _publish_instagram(self, video_path: str, title: str, description: str) -> Dict[str, Any]:
        """Publish to Instagram Reels via Graph API"""
        try:
            if not self.instagram_access_token:
                self.logger.warning("⚠️ INSTAGRAM_ACCESS_TOKEN no configurado")
                return {
                    "platform": "instagram",
                    "upload_status": "skipped",
                    "reason": "API token not configured"
                }

            # Step 1: Upload video container
            url = "https://graph.instagram.com/v18.0/me/media"

            with open(video_path, 'rb') as f:
                files = {'video': f}
                data = {
                    'media_type': 'REELS',
                    'video_state': 'DRAFT',
                    'access_token': self.instagram_access_token,
                    'caption': f"{title}\n\n{description}"
                }

                response = requests.post(url, files=files, data=data, timeout=300)

            if response.status_code in [200, 201]:
                media_id = response.json().get("id")

                # Step 2: Publish the media
                publish_url = f"https://graph.instagram.com/v18.0/{media_id}"
                publish_data = {
                    'status': 'PUBLISHED',
                    'access_token': self.instagram_access_token
                }

                publish_response = requests.post(publish_url, data=publish_data, timeout=30)

                if publish_response.status_code in [200, 201]:
                    self.logger.info(f"✅ Instagram published: {media_id}")
                    return {
                        "platform": "instagram",
                        "video_id": media_id,
                        "video_url": f"https://www.instagram.com/reel/{media_id}/",
                        "upload_status": "published",
                        "published_at": datetime.now().isoformat()
                    }
                else:
                    self.logger.warning(f"⚠️ Instagram publish error: {publish_response.text}")
                    return {
                        "platform": "instagram",
                        "upload_status": "failed",
                        "error": publish_response.text[:200]
                    }
            else:
                self.logger.warning(f"⚠️ Instagram upload error: {response.status_code}")
                return {
                    "platform": "instagram",
                    "upload_status": "failed",
                    "error": response.text[:200]
                }

        except Exception as e:
            self.logger.error(f"❌ Instagram publish error: {str(e)}")
            return {
                "platform": "instagram",
                "upload_status": "error",
                "error": str(e)
            }

    async def _publish_youtube(
        self,
        video_path: str,
        title: str,
        description: str,
        tags: List[str],
        thumbnail_path: str = None
    ) -> Dict[str, Any]:
        """Publish to YouTube via YouTube Data API v3"""
        try:
            if not self.youtube_access_token:
                self.logger.warning("⚠️ YOUTUBE_ACCESS_TOKEN no configurado")
                return {
                    "platform": "youtube",
                    "upload_status": "skipped",
                    "reason": "API token not configured"
                }

            # YouTube API endpoint
            url = "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status"

            headers = {
                "Authorization": f"Bearer {self.youtube_access_token}",
                "X-Goog-Upload-Protocol": "resumable",
                "X-Goog-Upload-Header-Content-Length": str(os.path.getsize(video_path)),
                "Content-Type": "application/json"
            }

            # Prepare metadata
            body = {
                "snippet": {
                    "title": title[:100],
                    "description": description[:5000],
                    "tags": tags[:30],
                    "categoryId": "28"  # Science & Technology
                },
                "status": {
                    "privacyStatus": "public",
                    "selfDeclaredMadeForKids": False
                }
            }

            # Create resumable session
            session_response = requests.post(
                url,
                headers=headers,
                json=body,
                timeout=30
            )

            if session_response.status_code not in [200, 201]:
                self.logger.warning(f"⚠️ YouTube session error: {session_response.status_code}")
                return {
                    "platform": "youtube",
                    "upload_status": "failed",
                    "error": "Could not create upload session"
                }

            # Get upload URL from Location header
            upload_url = session_response.headers.get("Location")
            if not upload_url:
                self.logger.warning("⚠️ No upload URL from YouTube")
                return {
                    "platform": "youtube",
                    "upload_status": "failed",
                    "error": "No upload URL received"
                }

            # Upload video file
            with open(video_path, 'rb') as f:
                video_data = f.read()

            upload_headers = {
                "Content-Type": "video/mp4"
            }

            upload_response = requests.put(
                upload_url,
                headers=upload_headers,
                data=video_data,
                timeout=600
            )

            if upload_response.status_code in [200, 201]:
                video_data = upload_response.json()
                video_id = video_data.get("id", "unknown")

                self.logger.info(f"✅ YouTube published: {video_id}")
                return {
                    "platform": "youtube",
                    "video_id": video_id,
                    "video_url": f"https://www.youtube.com/watch?v={video_id}",
                    "upload_status": "published",
                    "published_at": datetime.now().isoformat()
                }
            else:
                self.logger.warning(f"⚠️ YouTube upload error: {upload_response.status_code}")
                return {
                    "platform": "youtube",
                    "upload_status": "failed",
                    "error": upload_response.text[:200]
                }

        except Exception as e:
            self.logger.error(f"❌ YouTube publish error: {str(e)}")
            return {
                "platform": "youtube",
                "upload_status": "error",
                "error": str(e)
            }


async def test_publisher():
    """Test del agente"""

    agent = Publisher(region="es")

    # Simulate a video from Agent 3
    test_video = "/tmp/test_video.mp4"
    if not os.path.exists(test_video):
        # Create dummy video for testing
        from pathlib import Path
        Path(test_video).touch()

    result = await agent.execute({
        "video_path": test_video,
        "title": "Test Video: AI News",
        "description": "Latest AI trends and news",
        "tags": ["AI", "technology", "news"],
        "platforms": ["tiktok", "instagram", "youtube"]
    })

    print("\n" + "=" * 60)
    print("📱 PUBLISHER TEST RESULT")
    print("=" * 60)
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        print(f"Platforms published: {result['result']['platforms_published']}")
        for r in result['result']['results']:
            print(f"  - {r['platform']}: {r['upload_status']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(test_publisher())
