[app]
title = Pyro Pyroland
package.name = pyrogame
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,ogg
version = 0.1

# Фиксируем стабильную комбинацию версий для работы Pygame на Android
requirements = python3==3.11.1, pygame==2.6.0, jnius

orientation = landscape
fullscreen = 1

android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

