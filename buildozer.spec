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
android.archs = arm64-v8a

# Фикс ошибки с лицензиями и версией build-tools
android.accept_sdk_license = True
android.build_tools_version = 33.0.0
android.ndk_api = 21

[buildozer]
log_level = 2
warn_on_root = 1
