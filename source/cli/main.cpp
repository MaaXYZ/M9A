#include <cstdio>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>

#include "MaaFramework/MaaAPI.h"

#include "meojson/json.hpp"
#include "utils/Locale.hpp"

struct Task
{
    std::string name;
    std::string type;
    json::value param = json::object();
};

using TaskList = std::vector<Task>;

void print_help();
bool proc_argv(int argc, char** argv, bool& debug, std::string& adb, std::string& adb_address, int& client_type,
               TaskList& tasks, MaaAdbControllerType& ctrl_type);
bool app_package_and_activity(int client_type, std::string& package, std::string& activity);
void save_config(const std::string& adb, const std::string& adb_address, int& client_type, const TaskList& tasks,
                 MaaAdbControllerType ctrl_type);
std::string read_adb_config(const std::filesystem::path& cur_dir);
void mpause();

int main(int argc, char** argv)
{
    print_help();

    bool debug = false;
    std::string adb = "adb";
    std::string adb_address = "127.0.0.1:5555";
    int client_type = 1;
    std::string package = "com.shenlan.m.reverse1999";
    std::string activity = "com.shenlan.m.reverse1999/com.ssgame.mobile.gamesdk.frame.AppStartUpActivity";
    TaskList tasks;
    MaaAdbControllerType control_type = 0;

    bool proced = proc_argv(argc, argv, debug, adb, adb_address, client_type, tasks, control_type);
    if (!proced) {
        std::cout << "Failed to parse argv" << std::endl;
        mpause();
        return -1;
    }
    bool identified = app_package_and_activity(client_type, package, activity);
    if (!identified) {
        std::cout << "Failed to identify the client type" << std::endl;
        mpause();
        return -1;
    }
    if (tasks.empty()) {
        std::cout << "Task empty" << std::endl;
        mpause();
        return -1;
    }

    const auto cur_dir = std::filesystem::path(argv[0]).parent_path();
    std::string debug_dir = (cur_dir / "debug").string();
    std::string resource_dir = (cur_dir / "resource").string();
    std::string adb_config = read_adb_config(cur_dir);

    MaaSetGlobalOption(MaaGlobalOption_Logging, (void*)debug_dir.c_str(), debug_dir.size());
    MaaSetGlobalOption(MaaGlobalOption_DebugMode, (void*)&debug, sizeof(bool));

    auto maa_handle = MaaCreate(nullptr, nullptr);
    auto resource_handle = MaaResourceCreate(nullptr, nullptr);
    auto controller_handle =
        MaaAdbControllerCreate(adb.c_str(), adb_address.c_str(), control_type, adb_config.c_str(), nullptr, nullptr);

    MaaBindResource(maa_handle, resource_handle);
    MaaBindController(maa_handle, controller_handle);
    int height = 720;
    MaaControllerSetOption(controller_handle, MaaCtrlOption_ScreenshotTargetShortSide, reinterpret_cast<void*>(&height),
                           sizeof(int));
    MaaControllerSetOption(controller_handle, MaaCtrlOption_DefaultAppPackageEntry, (void*)activity.c_str(),
                           activity.size());
    MaaControllerSetOption(controller_handle, MaaCtrlOption_DefaultAppPackage, (void*)package.c_str(), package.size());

    auto resource_id = MaaResourcePostPath(resource_handle, resource_dir.c_str());
    auto connection_id = MaaControllerPostConnection(controller_handle);

    MaaResourceWait(resource_handle, resource_id);
    MaaControllerWait(controller_handle, connection_id);

    auto destroy = [&]() {
        MaaDestroy(maa_handle);
        MaaResourceDestroy(resource_handle);
        MaaControllerDestroy(controller_handle);
    };

    if (!MaaInited(maa_handle)) {
        destroy();
        std::cout << "Failed to init Maa instance, a connection error or resource file corruption occurred, please "
                     "refer to the log."
                  << std::endl;
        mpause();
        return -1;
    }

    MaaTaskId task_id = 0;
    for (const auto& task : tasks) {
        task_id = MaaPostTask(maa_handle, task.type.c_str(), task.param.to_string().c_str());
    }
    MaaWaitTask(maa_handle, task_id);

    destroy();

    return 0;
}

void print_help()
{
    std::cout << utf8_to_crt(
                     R"(欢迎使用 MAA 1999 CLI, 源码地址：https://github.com/MaaAssistantArknights/MAA1999

用法: MAA1999.exe [adb路径] [adb地址] [任务名（有序）]...

可以修改 config.json 来配置任务

请注意命令行参数中的任务名请输入 name，而非 type。name 是可以自己随意修改的，但 type 是固定的。
若无命令行参数，则按顺序执行 config.json 中的全部任务。

欢迎大佬来给我们搓个 GUI _(:з」∠)_

v0.2.0
新增了全关卡导航支持，但还不会吃糖。引导只加了几个常用的关卡，有其他需求可以改改 config，复现次数也在 config 里改

)") << std::endl;
}

json::value combat_param(int index)
{
    json::value param;
    auto& diff = param["diff_task"];

    auto& chapter = diff["EnterTheShow"]["next"];
    auto& stage = diff["TargetStageName"]["text"];
    auto& difficulty = diff["StageDifficulty"]["next"];
    auto& times = diff["SetReplaysTimes"]["text"];
    auto& all_in = diff["AllIn"]["enabled"];
    auto& all_in_doc = diff["AllIn"]["doc"];
    auto& eat_candy_within_24h = diff["EatCandyWithin24H"]["enabled"];
    auto& eat_candy_within_24h_doc = diff["EatCandyWithin24H"]["doc"];
    
    all_in = false;
    all_in_doc = "刷活性；默认false";
    eat_candy_within_24h = false;
    eat_candy_within_24h_doc = "无限吃24小时内过期的糖；默认false，前置条件：开启刷活性";

    switch (index) {
    case 5:
        // "5. 3-9 厄险（百灵百验鸟）\n"
        chapter = "MainChapter_3";
        stage = "09";
        difficulty = "StageDifficulty_Hard";
        times = "1";
        break;
    case 6:
        // "6. 4-20 厄险（双头形骨架）\n"
        chapter = "MainChapter_4";
        stage = "20";
        difficulty = "StageDifficulty_Hard";
        times = "1";
        break;
    case 7:
        // "7. 2-3 厄险（祝圣秘银）\n"
        chapter = "MainChapter_2";
        stage = "03";
        difficulty = "StageDifficulty_Hard";
        times = "1";
        break;
    case 8:
        // "8. 3-13 厄险（盐封曼德拉）\n"
        chapter = "MainChapter_3";
        stage = "13";
        difficulty = "StageDifficulty_Hard";
        times = "1";
        break;
    case 9:
        // "9. 4-10 厄险（啮咬盒）\n"
        chapter = "MainChapter_4";
        stage = "10";
        difficulty = "StageDifficulty_Hard";
        times = "1";
        break;
    case 10:
        // "10. 3-11 厄险（金爪灵摆）\n"
        chapter = "MainChapter_3";
        stage = "11";
        difficulty = "StageDifficulty_Hard";
        times = "1";
        break;

    case 11:
        // "11. 尘埃运动 06\n"
        chapter = "ResourceChapter_LP";
        stage = "06";
        difficulty = "StageDifficulty_None";
        times = "1";
        break;
    case 12:
        // "12. 猪鼻美学 06\n"
        chapter = "ResourceChapter_MA";
        stage = "06";
        difficulty = "StageDifficulty_None";
        times = "1";
        break;
    case 13:
        // "13. 丰收时令 04\n"
        chapter = "ResourceChapter_MA";
        stage = "04";
        difficulty = "StageDifficulty_None";
        times = "1";
        break;

    case 14:
        //"14. 群山之声 06（洞悉 岩）\n"
        chapter = "PromotionChapter_ME";
        stage = "06";
        difficulty = "StageDifficulty_None";
        times = "1";
        break;
    case 15:
        //"15. 星陨之所 06（洞悉 星）\n"
        chapter = "PromotionChapter_SL";
        stage = "06";
        difficulty = "StageDifficulty_None";
        times = "1";
        break;
    case 16:
        //"16. 深林之形 06（洞悉 林）\n"
        chapter = "PromotionChapter_SS";
        stage = "06";
        difficulty = "StageDifficulty_None";
        times = "1";
        break;
    case 17:
        //"17. 荒兽之野 06（洞悉 兽）\n"
        chapter = "PromotionChapter_BW";
        stage = "06";
        difficulty = "StageDifficulty_None";
        times = "1";
        break;

    case 18:
        //"18. 活动：绿湖噩梦 17 艰难\n"
        chapter = "ANightmareAtGreenLake";
        stage = "17";
        difficulty = "ActivityStageDifficulty";
        times = "1";
        break;

    case 19:
        //"19. 活动：行至摩卢旁卡 16 艰难\n"
        chapter = "JourneytoMorPankh";
        stage = "16";
        difficulty = "ActivityStageDifficulty";
        times = "1";
        break;
    }

    return param;
}

bool app_package_and_activity(int client_type, std::string& package, std::string& activity)
{
    switch (client_type) {
    case 1:
        //"1. 官服\n"
        package = "com.shenlan.m.reverse1999";
        activity = "com.shenlan.m.reverse1999/com.ssgame.mobile.gamesdk.frame.AppStartUpActivity";
        break;
    case 2:
        //"1. B服\n"
        package = "com.shenlan.m.reverse1999.bilibili";
        activity = "com.shenlan.m.reverse1999.bilibili/com.ssgame.mobile.gamesdk.frame.AppStartUpActivity";
        break;
    default:
        return false;
    }

    return true;
}

bool proc_argv(int argc, char** argv, bool& debug, std::string& adb, std::string& adb_address, int& client_type,
               TaskList& tasks, MaaAdbControllerType& ctrl_type)
{
    int touch = 1;
    int key = 1;
    int screencap = 3;

    tasks.clear();

    if (auto config_opt = json::open("config.json")) {
        auto& confing = *config_opt;

        debug = confing.get("debug", false);
        adb = confing["adb"].as_string();
        adb_address = confing["adb_address"].as_string();
        client_type = confing.get("client", client_type);

        int index = 1;
        for (auto& task : confing["tasks"].as_array()) {
            Task task_obj;
            if (task.is_string()) {
                task_obj.type = task.as_string();
                task_obj.name = "MyTask" + std::to_string(index++);
            }
            else {
                task_obj.type = task["type"].as_string();
                task_obj.name = task["name"].as_string();
                task_obj.param = task["param"];
            }
            tasks.emplace_back(task_obj);
        }
        touch = confing.get("touch", touch);
        key = confing.get("key", key);
        screencap = confing.get("screencap", screencap);

        ctrl_type = touch << 0 | key << 8 | screencap << 16;
    }
    else {
        std::cout << std::endl
                  << std::endl
                  << utf8_to_crt("请输入 adb 路径，例如 C:/adb.exe，不要有中文: ") << std::endl;
        std::getline(std::cin, adb);
        std::cout << std::endl << std::endl << utf8_to_crt("请输入 adb 地址，例如 127.0.0.1:5555：") << std::endl;
        std::getline(std::cin, adb_address);
        std::cout << std::endl
                  << std::endl
                  << utf8_to_crt("选择客户端类型：") << std::endl
                  << std::endl
                  << utf8_to_crt("1. 官服\n"
                                 "2. Bilibili服\n")
                  << std::endl
                  << std::endl
                  << utf8_to_crt("请输入客户端类型序号，例如 1: ") << std::endl;
        std::string client_type_tmp;
        std::getline(std::cin, client_type_tmp);
        client_type = std::stoi(client_type_tmp);
        if (1 > client_type || client_type > 2) {
            std::cout << "Unknown Client Type: " << client_type << std::endl;
            return false;
        }
        std::cout << std::endl
                  << std::endl
                  << utf8_to_crt("选择任务，会自动登录，但不会启动模拟器") << std::endl
                  << std::endl
                  << utf8_to_crt("1. 启动游戏\n"
                                 "2. 收取荒原\n"
                                 "3. 领取奖励\n"
                                 "4. 每日心相（意志解析）\n"
                                 "5. 3-9 厄险（百灵百验鸟）\n"
                                 "6. 4-20 厄险（双头形骨架）\n"
                                 "7. 2-3 厄险（祝圣秘银）\n"
                                 "8. 3-13 厄险（盐封曼德拉）\n"
                                 "9. 4-10 厄险（啮咬盒）\n"
                                 "10. 3-11 厄险（金爪灵摆）\n"
                                 "11. 尘埃运动 06\n"
                                 "12. 猪鼻美学 06\n"
                                 "13. 丰收时令 04\n"
                                 "14. 群山之声 06（洞悉 岩）\n"
                                 "15. 星陨之所 06（洞悉 星）\n"
                                 "16. 深林之形 06（洞悉 林）\n"
                                 "17. 荒兽之野 06（洞悉 兽）\n"
                                 "18. 活动：绿湖噩梦 17 艰难（活动已结束）\n"
                                 "19. 活动：行至摩卢旁卡 16 艰难\n")
                  << std::endl
                  << std::endl
                  << utf8_to_crt("请输入要执行的任务序号，可自定义顺序，以空格分隔，例如 1 2 4 12 3: ") << std::endl;
        std::vector<int> task_ids;
        std::string line;
        std::getline(std::cin, line);
        std::istringstream iss(line);
        int task_id;
        while (iss >> task_id) {
            task_ids.emplace_back(task_id);
        }

        // tasks.emplace_back(Task { .name = "MyTask0", .type = "Start1999" });

        int index = 1;
        for (auto id : task_ids) {
            Task task_obj;
            task_obj.name = "MyTask" + std::to_string(index++);

            switch (id) {
            case 1:
                task_obj.type = "StartUp";
                break;
            case 2:
                task_obj.type = "Wilderness";
                break;
            case 3:
                task_obj.type = "Awards";
                break;

            case 4:
                task_obj.type = "Psychube";
                break;

            case 5:
            case 6:
            case 7:
            case 8:
            case 9:
            case 10:
            case 11:
            case 12:
            case 13:
            case 14:
            case 15:
            case 16:
            case 17:
                task_obj.type = "Combat";
                task_obj.param = combat_param(id);
                break;

            case 18:
                task_obj.type = "ANightmareAtGreenLake";
                task_obj.param = combat_param(id);
                break;

            case 19:
                task_obj.type = "JourneytoMorPankh";
                task_obj.param = combat_param(id);
                break;

            default:
                std::cout << "Unknown task: " << id << std::endl;
                return false;
            }
            tasks.emplace_back(std::move(task_obj));
        }

        ctrl_type = touch << 0 | key << 8 | screencap << 16;
        save_config(adb, adb_address, client_type, tasks, ctrl_type);
    }

    if (argc >= 3) {
        adb = argv[1];
        adb_address = argv[2];

        std::vector<std::string> task_names;
        for (int i = 3; i < argc; ++i) {
            task_names.emplace_back(argv[i]);
        }
        auto all_tasks = std::move(tasks);
        tasks.clear();
        for (auto& task_name : task_names) {
            for (auto& task : all_tasks) {
                if (task.name == task_name) {
                    tasks.emplace_back(task);
                    break;
                }
            }
        }
    }

    return true;
}

void save_config(const std::string& adb, const std::string& adb_address, int& client_type, const TaskList& tasks,
                 MaaAdbControllerType ctrl_type)
{
    json::value config;
    config["debug"] = false;
    config["adb"] = adb;
    config["adb_Doc"] = "adb.exe 所在路径，相对绝对均可";
    config["adb_address"] = adb_address;
    config["adb_address_Doc"] = "adb 连接地址，例如 127.0.0.1:5555";
    config["client_type"] = client_type;
    config["client_type_Doc"] = "客户端类型：1: 官服, 2: Bilibili服";

    json::value tasks_array;
    for (auto& task : tasks) {
        json::value task_obj;
        task_obj["type"] = task.type;
        task_obj["name"] = task.name;
        task_obj["param"] = task.param;
        tasks_array.emplace(std::move(task_obj));
    }
    config["tasks"] = std::move(tasks_array);
    config["tasks_Doc"] = "要执行的任务 StartUp, Wilderness, Psychube, Awards, Combat";

    config["touch"] = (ctrl_type & MaaAdbControllerType_Touch_Mask) >> 0;
    config["touch_Doc"] = "点击方式：1: Adb, 2: MiniTouch, 3: MaaTouch";
    // config["key"] = key;
    // config["key_Doc"] = "按键方式：1: Adb, 2: MaaTouch";
    config["screencap"] = (ctrl_type & MaaAdbControllerType_Screencap_Mask) >> 16;
    config["screencap_Doc"] = "截图方式：1: 自动测速, 2: RawByNetcat, 3: RawWithGzip, 4: Encode, 5: EncodeToFile, 6: "
                              "MinicapDirect, 7: MinicapStream";
    config["version"] = "v0.2.0";

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

void mpause()
{
    std::ignore = getchar();
}