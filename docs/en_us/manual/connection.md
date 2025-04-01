# Connection Settings

- [Connection Settings](#connection-settings)
  - [Auto Detect](#auto-detect)
  - [ADB Path](#adb-path)
    - [Using ADB Provided by Emulator](#using-adb-provided-by-emulator)
    - [Using ADB Provided by Google](#using-adb-provided-by-google)
  - [Connection Address](#connection-address)
    - [Emulator Documentation and Reference Addresses](#emulator-documentation-and-reference-addresses)
    - [Getting Multi-Instance Ports](#getting-multi-instance-ports)
  - [Touch Control Mode](#touch-control-mode)
  - [M9A and Emulator Multi-Instance](#m9a-and-emulator-multi-instance)
  - [MFAWPF/MFAAvalonia Specific Settings](#mfawpfmfaavalonia-specific-settings)
    - [ADB Extra Parameters](#adb-extra-parameters)
    - [Emulator Additional Commands (Optional)](#emulator-additional-commands-optional)

## Auto Detect

M9A can automatically detect and fill in the ADB path, connection address, and connection configuration based on the **single currently running emulator**.

As of M9A v2.5.7, supported emulators and their connection addresses for auto-detection are:

- MuMu Player 12: `127.0.0.1:16384/16416/16448/16480/16512/16544/16576`
- LDPlayer 9: `emulator-5554/5556/5558/5560`, `127.0.0.1:5555/5557/5559/5561`
- BlueStacks 5: `127.0.0.1:5555/5556/5565/5575/5585/5595/5554`
- NoxPlayer: `127.0.0.1:62001/59865`
- MEmu Player (逍遥模拟器): `127.0.0.1:21503`

> [!NOTE]
>
> The '/' above means "or". Please choose based on your actual situation, don't write them all!

If detection fails, try launching M9A with UAC administrator privileges and detect again. If it still fails, please refer to the manual setup instructions below and confirm if your emulator and connection address are in the list above.

## ADB Path

> [!NOTE]
>
> Auto-detection uses the emulator's ADB, but sometimes it fails. Manual setup is then required.
> `Force Replace ADB` downloads Google's ADB and replaces the existing one. Setting up Google's ADB yourself provides a permanent solution.

### Using ADB Provided by Emulator

Navigate to the emulator's installation path. On Windows, you can right-click the emulator process in Task Manager while it's running and select `Open file location`.

There should be an `.exe` file with `adb` in its name in the top-level or a sub-directory. You can use the search function, then select it.

> [!NOTE]
>
> Some examples:
> `adb.exe` `HD-adb.exe` `adb_server.exe` `nox_adb.exe`

### Using ADB Provided by Google

[Click to download](https://dl.google.com/android/repository/platform-tools-latest-windows.zip), extract the archive, and then select `adb.exe` from within.

It's recommended to extract it directly into the M9A folder. This allows you to simply enter `.\platform-tools\adb.exe` as the ADB path, and it can be moved together with the M9A folder.

## Connection Address

> [!TIP]
>
> The connection address for an emulator running on the local machine should be `127.0.0.1:<PortNumber>` or `emulator-<FourDigitNumber>`.

### Emulator Documentation and Reference Addresses

- [Bluestacks 5](https://support.bluestacks.com/hc/en-us/articles/360059480631-How-to-connect-to-BlueStacks-5-using-Android-Debug-Bridge-ADB-) `127.0.0.1:5555` (or check settings)
- [MuMu Player Pro (Mac)](https://mumu.163.com/mac/function/20240126/40028_1134600.html) `127.0.0.1:16384`
- [MuMu Player 12 (Windows)](https://mumu.163.com/help/20230214/35047_1073151.html) `127.0.0.1:16384`
- [LDPlayer 9](https://www.ldplayer.net/blog/how-to-connect-ldplayer-with-adb.html) `emulator-5554` (or check multi-instance manager)
- [NoxPlayer](https://support.bignox.com/en/qt/ml) `127.0.0.1:62001`
- [MEmu Player (逍遥模拟器)](https://bbs.xyaz.cn/forum.php?mod=viewthread&tid=365537) `127.0.0.1:21503`

For other emulators, you can refer to [Zhao Qingqing's blog post](https://www.cnblogs.com/zhaoqingqing/p/15238464.html) (Chinese).

### Getting Multi-Instance Ports

- MuMu 12 Multi-instance manager shows the ports of running instances in the top right corner.
- Bluestacks 5 emulator settings allow viewing the current instance's port.
- LDPlayer 9 Multi-instance manager shows the ADB address/port.
- _To be supplemented_

> [!NOTE]
>
> Alternative Methods
>
> - Method 1: Use ADB command to view emulator ports
>
>   1. Start **one** emulator and ensure no other Android devices are connected to the computer.
>   2. Open a terminal in the folder containing the ADB executable.
>   3. Execute the following command.
>
>   ```sh
>   # Windows Command Prompt
>   adb devices
>   # Windows PowerShell
>   .\adb devices
>   ```
>
>   Example output:
>
>   ```text
>   List of devices attached
>   127.0.0.1:<PortNumber>   device
>   emulator-<FourDigitNumber>  device
>   ```
>
>   Use `127.0.0.1:<PortNumber>` or `emulator-<FourDigitNumber>` as the connection address.
>
> - Method 2: Find established ADB connections (Windows)
>
>   1. Perform Method 1.
>   2. Press `Win+S`, type `Resource Monitor`, and open it.
>   3. Switch to the `Network` tab. In the `Listening Ports` section, find the emulator process name (e.g., `HD-Player.exe`) in the Image column.
>   4. Note down all listening ports for the emulator process.
>   5. In the `TCP Connections` section, find `adb.exe` in the Image column. The port listed in the `Remote Port` column that matches one of the emulator's listening ports is the emulator's debug port.

## Touch Control Mode

1. [Minitouch](https://github.com/DeviceFarmer/minitouch): An Android touch event injector written in C. It operates `evdev` devices and provides a socket interface for external programs to trigger touch events and gestures. Starting from Android 10, Minitouch is no longer available when SELinux is in `Enforcing` mode.<sup>[Source](https://github.com/DeviceFarmer/minitouch?tab=readme-ov-file#for-android-10-and-up)</sup>
2. [MaaTouch](https://github.com/MaaAssistantArknights/MaaTouch): A reimplementation of Minitouch in Java by MAA, using the native Android `InputDevice` and adding extra features. Usability on higher Android versions is yet to be tested. ~~Help us test it~~
3. Adb Input: Directly calls ADB to use Android's `input` command for touch operations. It offers the highest compatibility but is the slowest.

## M9A and Emulator Multi-Instance

> [!NOTE]
> If you need to run multiple emulator instances simultaneously, you can copy the M9A folder multiple times. Use **different M9A instances**, the **same adb.exe**, and **different connection addresses** to connect to each emulator instance.

## MFAWPF/MFAAvalonia Specific Settings

### ADB Extra Parameters

**Generally, you don't need to modify this; keep it as `{}`.**

This corresponds to the `"AdbDevice"` `"Config"` field value in `debug/config.json`,
e.g., `{"extras":{"mumu":{"enable":true,"index":0,"path":"D:/Program Files/Netease/MuMu Player 12"}}}` or `{"extras":{"ld":{"enable":true,"index":1,"path":"C:/leidian/LDPlayer9","pid":7524}}}`.

### Emulator Additional Commands (Optional)

This parameter is used for automatically starting/stopping the emulator. You can find it in Settings -> Startup Settings. Configure it according to your needs.

| Brand     | Launch Parameter          |
| --------- | ------------------------- |
| MuMu      | `-v <instance_index>`     |
| LDPlayer  | `index=<instance_index>`  |

> [!NOTE]
>
> `<instance_index>` should be replaced entirely when filling it in (index starts from 0). Pay attention to spaces.
