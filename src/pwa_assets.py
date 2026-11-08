# src/pwa_assets.py — Generates PWA manifest, service worker, and standalone icons
# Usage: python src/pwa_assets.py
# Requires: os, json, zlib, struct

import os
import json
import zlib
import struct

def create_png(width: int, height: int, filepath: str):
    """Generates a standalone dark-theme radar icon as a valid PNG without third-party dependencies."""
    # Header: 8-byte PNG signature
    png_sig = b"\x89PNG\r\n\x1a\n"
    
    # IHDR chunk
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0) # 8-bit truecolor RGB
    ihdr_crc = struct.pack(">I", zlib.crc32(b"IHDR" + ihdr_data))
    ihdr_chunk = struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + ihdr_crc

    # Raw pixel data (RGB with 1 filter byte per scanline)
    # Background: #090d16 -> (9, 13, 22)
    # Accent: #38bdf8 -> (56, 189, 248)
    # Muted: #23314a -> (35, 49, 74)
    # Core: #10b981 -> (16, 185, 129)
    center_x = width / 2.0
    center_y = height / 2.0
    max_radius = width * 0.42

    raw_scanlines = []
    for y in range(height):
        scanline = bytearray([0]) # Filter byte 0 (None)
        for x in range(width):
            dx = x - center_x
            dy = y - center_y
            dist = (dx * dx + dy * dy) ** 0.5

            r, g, b = 9, 13, 22 # Default dark background

            # Draw outer radar ring
            if abs(dist - max_radius) < (width * 0.015):
                r, g, b = 35, 49, 74
            # Draw middle radar ring
            elif abs(dist - (max_radius * 0.65)) < (width * 0.015):
                r, g, b = 56, 189, 248
            # Draw inner radar ring
            elif abs(dist - (max_radius * 0.35)) < (width * 0.015):
                r, g, b = 35, 49, 74
            # Draw center blip / target dot
            elif dist < (width * 0.08):
                r, g, b = 56, 189, 248
            # Draw radar sweep line / crosshair
            elif (abs(dx) < 1.5 or abs(dy) < 1.5) and dist <= max_radius:
                r, g, b = 25, 38, 58
            # Draw high-priority ping
            elif ((x - (center_x + max_radius * 0.45))**2 + (y - (center_y - max_radius * 0.35))**2)**0.5 < (width * 0.045):
                r, g, b = 16, 185, 129

            scanline.extend([r, g, b])
        raw_scanlines.append(bytes(scanline))

    compressed_idat = zlib.compress(b"".join(raw_scanlines), level=9)
    idat_crc = struct.pack(">I", zlib.crc32(b"IDAT" + compressed_idat))
    idat_chunk = struct.pack(">I", len(compressed_idat)) + b"IDAT" + compressed_idat + idat_crc

    # IEND chunk
    iend_chunk = struct.pack(">I", 0) + b"IEND" + struct.pack(">I", zlib.crc32(b"IEND"))

    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "wb") as f:
        f.write(png_sig + ihdr_chunk + idat_chunk + iend_chunk)

def create_svg(filepath: str):
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
  <rect width="512" height="512" rx="112" fill="#090d16"/>
  <circle cx="256" cy="256" r="190" fill="none" stroke="#23314a" stroke-width="6"/>
  <circle cx="256" cy="256" r="125" fill="none" stroke="#38bdf8" stroke-width="5" stroke-dasharray="10 8"/>
  <circle cx="256" cy="256" r="60" fill="none" stroke="#23314a" stroke-width="4"/>
  <line x1="256" y1="66" x2="256" y2="446" stroke="#1a273f" stroke-width="3"/>
  <line x1="66" y1="256" x2="446" y2="256" stroke="#1a273f" stroke-width="3"/>
  <circle cx="256" cy="256" r="18" fill="#38bdf8"/>
  <circle cx="340" cy="190" r="14" fill="#10b981"/>
  <circle cx="340" cy="190" r="28" fill="none" stroke="#10b981" stroke-width="2" opacity="0.6"/>
</svg>"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(svg_content)

def generate_manifest(dirpath: str):
    manifest = {
        "name": "Sayari Compliance Signal Radar",
        "short_name": "Sayari Radar",
        "description": "Living psychographic signal bank and content ideas for compliance officers and investigations analysts.",
        "start_url": "./index.html",
        "scope": "./",
        "display": "standalone",
        "background_color": "#090d16",
        "theme_color": "#090d16",
        "orientation": "any",
        "icons": [
            {
                "src": "icons/icon-192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "icons/icon-512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "icons/icon.svg",
                "sizes": "any",
                "type": "image/svg+xml",
                "purpose": "any"
            }
        ]
    }
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

def generate_service_worker(dirpath: str):
    sw_code = """// Sayari Radar Service Worker — Offline Caching & Instant Loads
const CACHE_NAME = 'sayari-radar-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './manifest.json',
  './icons/icon-192.png',
  './icons/icon-512.png',
  './icons/icon.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Network-first strategy for real-time compliance pulse, falling back to cached offline state
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            return cachedResponse;
          }
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });
      })
  );
});
"""
    os.makedirs(dirpath, exist_ok=True)
    with open(os.path.join(dirpath, "sw.js"), "w", encoding="utf-8") as f:
        f.write(sw_code)

def build_all_pwa_assets(target_dirs: list[str]):
    for d in target_dirs:
        generate_manifest(d)
        generate_service_worker(d)
        create_png(192, 192, os.path.join(d, "icons", "icon-192.png"))
        create_png(512, 512, os.path.join(d, "icons", "icon-512.png"))
        create_svg(os.path.join(d, "icons", "icon.svg"))
        print(f"[pwa] Generated PWA manifest, service worker & icons in: {d}")

if __name__ == "__main__":
    build_all_pwa_assets(["viewer", "docs"])
