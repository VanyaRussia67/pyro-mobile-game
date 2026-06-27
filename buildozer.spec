[app]
title = Pyro Pyroland
package.name = pyrogame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ogg
version = 0.1
requirements = python3,pygame
orientation = landscape
fullscreen = 1

# Исправленные архитектуры и версии API под новые требования Google
android.archs = arm64-v8a, armeabi-v7a
android.api = 34
android.minapi = 24
android.ndk = 26b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
