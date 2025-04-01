# Project Structure

- [Project Structure](#project-structure)
  - [`.github`](#github)
    - [`.github/ISSUE_TEMPLATE`](#githubissue_template)
    - [`.github/workflows`](#githubworkflows)
    - [`.github/cliff.toml`](#githubclifftoml)
  - [`.vscode`](#vscode)
  - [`agent`](#agent)
    - [`agent/custom`](#agentcustom)
      - [`agent/custom/action`](#agentcustomaction)
      - [`agent/custom/reco`](#agentcustomreco)
    - [`agent/utils`](#agentutils)
    - [`agent/main.py`](#agentmainpy)
  - [`assets`](#assets)
    - [`assets/MaaCommonAssets`](#assetsmaacommonassets)
    - [`assets/resource`](#assetsresource)
      - [`assets/resource/base`](#assetsresourcebase)
        - [`assets/resource/base/image`](#assetsresourcebaseimage)
        - [`assets/resource/base/model`](#assetsresourcebasemodel)
        - [`assets/resource/base/pipeline`](#assetsresourcebasepipeline)
        - [`assets/resource/base/default_pipeline.json`](#assetsresourcebasedefault_pipelinejson)
      - [`assets/resource/bilibili`](#assetsresourcebilibili)
      - [`assets/resource/global_en`](#assetsresourceglobal_en)
      - [`assets/resource/global_jp`](#assetsresourceglobal_jp)
      - [`assets/resource/cn.json`](#assetsresourcecnjson)
      - [`assets/resource/en.json`](#assetsresourceenjson)
      - [`assets/resource/jp.json`](#assetsresourcejpjson)
    - [`assets/interface.json`](#assetsinterfacejson)
  - [`deps`](#deps)
  - [`docs`](#docs)
    - [`docs/zh_cn`](#docszh_cn)
      - [`docs/zh_cn/develop`](#docszh_cndevelop)
      - [`docs/zh_cn/manual`](#docszh_cnmanual)
    - [`docs/en_us`](#docsen_us)
      - [`docs/en_us/develop`](#docsen_usdevelop)
      - [`docs/en_us/manual`](#docsen_usmanual)
    - [`docs/.markdownlint.yaml`](#docsmarkdownlintyaml)
  - [`tools`](#tools)
    - [`tools/ci`](#toolsci)
    - [`tools/configure.py`](#toolsconfigurepy)
    - [`tools/install.py`](#toolsinstallpy)
  - [`.gitignore`](#gitignore)
  - [`.gitmodules`](#gitmodules)
  - [`.pre-commit-config.yaml`](#pre-commit-configyaml)
  - [`.prettierrc`](#prettierrc)
  - [`LICENSE`](#license)
  - [`package-lock.json&package.json`](#package-lockjsonpackagejson)
  - [`README.md`](#readmemd)
  - [`requirements.txt`](#requirementstxt)

Below is the project structure and its description.

## `.github`

GitHub configuration.

### `.github/ISSUE_TEMPLATE`

GitHub issue templates.

### `.github/workflows`

GitHub workflow configurations.

### `.github/cliff.toml`

Cliff configuration (used for automatically generating release notes).

## `.vscode`

VSCode configuration.

## `agent`

Contains code related to the agent.

### `agent/custom`

Custom actions/recognition.

#### `agent/custom/action`

Custom actions.

#### `agent/custom/reco`

Custom recognition.

### `agent/utils`

Utility functions.

### `agent/main.py`

Processes before starting the agent and starts the AgentServer.

## `assets`

Contains project resource files.

### `assets/MaaCommonAssets`

Contains Maa common resources, such as OCR models.

### `assets/resource`

Contains project resource files.

#### `assets/resource/base`

Contains official server resources, which serve as the base for other server resources.

##### `assets/resource/base/image`

Contains template images.

##### `assets/resource/base/model`

Contains OCR models, neural network classification models, and neural network detection models. [Cooking Guide](https://github.com/MaaXYZ/MaaNeuralNetworkCookbook)

##### `assets/resource/base/pipeline`

JSON files describing task pipelines, written according to the [Task Pipeline Protocol](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/3.1-%E4%BB%BB%E5%8A%A1%E6%B5%81%E6%B0%B4%E7%BA%BF%E5%8D%8F%E8%AE%AE.md).

##### `assets/resource/base/default_pipeline.json`

Sets default properties in the pipeline, refer to [default_pipeline.json](https://github.com/MaaXYZ/MaaFramework/blob/main/sample/resource/default_pipeline.json).

#### `assets/resource/bilibili`

Contains resources for the Bilibili server, overriding official server resources.

#### `assets/resource/global_en`

Contains resources for the global English server, overriding official and Japanese server resources.

#### `assets/resource/global_jp`

Contains resources for the Japanese server, overriding official server resources.

#### `assets/resource/cn.json`

Contains activity information for the CN server.

#### `assets/resource/en.json`

Contains activity information for the EN server.

#### `assets/resource/jp.json`

Contains activity information for the JP server.

### `assets/interface.json`

A standardized project structure declaration for MaaFramework, following the [Project Interface Protocol](https://github.com/MaaXYZ/MaaFramework/blob/main/docs/zh_cn/3.2-ProjectInterface%E5%8D%8F%E8%AE%AE.md).

## `deps`

Contains dependencies (extract the MaaFramework release package here).

## `docs`

User manuals and development documentation.

### `docs/zh_cn`

Chinese documentation.

#### `docs/zh_cn/develop`

Chinese Development documentation.

#### `docs/zh_cn/manual`

Chinese User manuals.

### `docs/en_us`

English documentation.

#### `docs/en_us/develop`

English Development documentation.

#### `docs/en_us/manual`

English User manuals.

### `docs/.markdownlint.yaml`

Markdownlint configuration.

## `tools`

Project tools.

### `tools/ci`

Tools used only in CI.

### `tools/configure.py`

Configuration tool, copies MaaCommonAssets to the resource directory.

### `tools/install.py`

Installation tool, assembles source code and dependencies into the `install` directory.

## `.gitignore`

Git ignore list.

## `.gitmodules`

Git submodules.

## `.pre-commit-config.yaml`

Pre-commit configuration.

## `.prettierrc`

Prettier configuration file.

## `LICENSE`

Open source license.

## `package-lock.json&package.json`

Prettier dependencies.

## `README.md`

Project description.

## `requirements.txt`

Dependencies required for the agent (Python).
