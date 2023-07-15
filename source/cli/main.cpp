#include "MaaAPI.h"

#include "Utils/Locale.hpp" // 不应该 include 这鬼玩意，图方便，先凑合用吧
#include <meojson/json.hpp>

#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

void print_help();
bool proc_argv(int argc, char** argv, std::string& adb, std::string& adb_address, std::vector<std::string>& tasks,
               MaaAdbControllerType& ctrl_type);
void save_config(const std::string& adb, const std::string& adb_address, const std::vector<std::string>& tasks,
                 MaaAdbControllerType ctrl_type);
std::string read_adb_config(const std::filesystem::path& cur_dir);
void pause();

int main(int argc, char** argv)
{
    print_help();

    std::string adb = "adb";
    std::string adb_address = "127.0.0.1:5555";
    std::vector<std::string> tasks;
    MaaAdbControllerType control_type = 0;

    bool proced = proc_argv(argc, argv, adb, adb_address, tasks, control_type);
    if (!proced) {
        std::cout << "Failed to parse argv" << std::endl;
        pause();
        return -1;
    }
    if (tasks.empty()) {
        std::cout << "Task empty" << std::endl;
        pause();
        return -1;
    }

    const auto cur_dir = std::filesystem::path(argv[0]).parent_path();
    std::string debug_dir = (cur_dir / "debug").string();
    std::string cache_dir = (cur_dir / "cache").string();
    std::string resource_dir = (cur_dir / "resource").string();
    std::string adb_config = read_adb_config(cur_dir);

    MaaSetGlobalOption(MaaGlobalOption_Logging, (void*)debug_dir.c_str(), debug_dir.size());

    auto maa_handle = MaaCreate(nullptr, nullptr);
    auto resource_handle = MaaResourceCreate(cache_dir.c_str(), nullptr, nullptr);
    auto controller_handle =
        MaaAdbControllerCreate(adb.c_str(), adb_address.c_str(), control_type, adb_config.c_str(), nullptr, nullptr);

    MaaBindResource(maa_handle, resource_handle);
    MaaBindController(maa_handle, controller_handle);
    int height = 720;
    MaaControllerSetOption(controller_handle, MaaCtrlOption_ScreenshotTargetHeight, reinterpret_cast<void*>(&height),
                           sizeof(int));

    auto resource_id = MaaResourcePostResource(resource_handle, resource_dir.c_str());
    auto connection_id = MaaControllerPostConnection(controller_handle);

    MaaResourceWait(resource_handle, resource_id);
    MaaControllerWait(controller_handle, connection_id);

    auto destroy = [&]() {
        MaaDestroy(&maa_handle);
        MaaResourceDestroy(&resource_handle);
        MaaControllerDestroy(&controller_handle);
    };

    if (!MaaInited(maa_handle)) {
        destroy();
        std::cout << "Failed to init Maa instance, a connection error or resource file corruption occurred, please "
                     "refer to the log."
                  << std::endl;
        pause();
        return -1;
    }

    save_config(adb, adb_address, tasks, control_type);

    for (const std::string& task : tasks) {
        auto task_id = MaaPostTask(maa_handle, task.c_str(), MaaTaskParam_Empty);
        MaaTaskWait(maa_handle, task_id);
    }

    destroy();

    return 0;
}

void print_help()
{
    std::cout << MAA_NS::utf8_to_stdout(
                     R"(欢迎使用 MAA 1999 CLI, 源码地址：https://github.com/MaaAssistantArknights/MAA1999

用法: MAA1999.exe [adb路径] [adb地址] [任务名] ...

也可以修改 config.json 来进行相关配置（命令行参数优先于 config.json）

欢迎大佬来给我们搓个 GUI _(:з」∠)_
)") << std::endl;
}

bool proc_argv(int argc, char** argv, std::string& adb, std::string& adb_address, std::vector<std::string>& tasks,
               MaaAdbControllerType& ctrl_type)
{
    int touch = 1;
    int key = 1;
    int screencap = 3;

    if (argc >= 3) {
        adb = argv[1];
        adb_address = argv[2];

        for (int i = 3; i < argc; ++i) {
            tasks.emplace_back(argv[i]);
        }
    }
    else if (auto config_opt = json::open("config.json")) {
        auto& confing = *config_opt;

        adb = confing["adb"].as_string();
        adb_address = confing["adb_address"].as_string();
        for (auto& task : confing["tasks"].as_array()) {
            tasks.emplace_back(task.as_string());
        }
        touch = confing.get("touch", touch);
        key = confing.get("key", key);
        screencap = confing.get("screencap", screencap);
    }
    else {
        std::cout << std::endl
                  << std::endl
                  << MAA_NS::utf8_to_stdout("请输入 adb 路径，例如 C:/adb.exe，不要有中文: ") << std::endl;
        std::getline(std::cin, adb);
        std::cout << std::endl
                  << std::endl
                  << MAA_NS::utf8_to_stdout("请输入 adb 地址，例如 127.0.0.1:5555：") << std::endl;
        std::getline(std::cin, adb_address);
        std::cout << std::endl
                  << std::endl
                  << MAA_NS::utf8_to_stdout("选择任务，会自动启动游戏及登录，但不会启动模拟器") << std::endl
                  << std::endl
                  << MAA_NS::utf8_to_stdout("1.收取荒原\n2.每日心相\n3.领取奖励") << std::endl
                  << std::endl
                  << MAA_NS::utf8_to_stdout("请输入要执行的任务序号，可自定义顺序，以空格分隔，例如 1 2 3: ")
                  << std::endl;
        std::vector<int> task_ids;
        std::string line;
        std::getline(std::cin, line);
        std::istringstream iss(line);
        int task_id;
        while (iss >> task_id) {
            task_ids.emplace_back(task_id);
        }
        for (auto id : task_ids) {
            switch (id) {
            case 1:
                tasks.emplace_back("Wilderness");
                break;
            case 2:
                tasks.emplace_back("Psychube");
                break;
            case 3:
                tasks.emplace_back("Awards");
                break;
            default:
                std::cout << "Unknown task: " << task_id << std::endl;
                return false;
            }
        }
    }

    ctrl_type = touch << 0 | key << 8 | screencap << 16;

    return true;
}

void save_config(const std::string& adb, const std::string& adb_address, const std::vector<std::string>& tasks,
                 MaaAdbControllerType ctrl_type)
{
    json::value config;
    config["adb"] = adb;
    config["adb_Doc"] = "adb.exe 所在路径，相对绝对均可";
    config["adb_address"] = adb_address;
    config["adb_address_Doc"] = "adb 连接地址，例如 127.0.0.1:5555";
    config["tasks"] = json::array(tasks);
    config["tasks_Doc"] = "要执行的任务，Wilderness, Psychube, Awards";
    config["touch"] = ctrl_type & MaaAdbControllerType_Touch_Mask;
    config["touch_Doc"] = "点击方式：1: Adb, 2: MiniTouch, 3: MaaTouch";
    // config["key"] = key;
    // config["key_Doc"] = "按键方式：1: Adb, 2: MaaTouch";
    config["screencap"] = ctrl_type & MaaAdbControllerType_Screencap_Mask;
    config["screencap_Doc"] = "截图方式：1: 自动测速, 2: RawByNetcat, 3: RawWithGzip, 4: Encode, 5: EncodeToFile, 6: "
                              "MinicapDirect, 7: MinicapStream";

    std::ofstream ofs("config.json", std::ios::out);
    ofs << config;
    ofs.close();
}

std::string read_adb_config(const std::filesystem::path& cur_dir)
{
    std::ifstream ifs(cur_dir / "resource" / "controller_config.json", std::ios::in);
    if (!ifs.is_open()) {
        std::cout << "Can't open controller_config.json" << std::endl;
        exit(1);
    }

    std::stringstream buffer;
    buffer << ifs.rdbuf();
    return buffer.str();
}

void pause()
{
    std::ignore = getchar();
}