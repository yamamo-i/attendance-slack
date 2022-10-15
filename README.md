# attendance-slack

* Slackのbot.
  * slackに特定のコメントが付くと, Akashiと連携して出退勤をする
* AkashiのAPIは以下
  * https://akashi.zendesk.com/hc/ja/sections/115000138574-%E5%85%AC%E9%96%8BAPI

## Usage

### setup

* poetryのインストール
  * ref: https://github.com/python-poetry/poetry#installation
* libraryのインストール
  
    ```shell
    $ poetry install
    ```
### 起動

* 設定ファイルの編集
  
    ```shell
    $ cp envfile.sample envfile
    # envfileはDocker用の環境変数
    # localで起動するときはexportで設定するように修正する
    $ [editor] envfile
    ```

### docker

#### dockerhubにupload済みのdocker imageで起動

* docker hubにimageをアップロード済み
    https://hub.docker.com/repository/docker/yamamoi/attendance-slack
* 起動
  
    ```shell
    $ docker run --env-file=envfile yamamoi/attendance-slack
    ```

#### localからdocker imageを作成して起動

* image作成

    ```shell
    $ docker build -t [image_name]:[tag_name] .
    ```

* 起動
  
    ```shell
    $ docker run --env-file=envfile [image_name]:[tag_name]
    ```

### local
* 起動
  
    ```shell
    $ source envfile_local
    $ python run.sh
    ```

### Kubernetes

検証したkubectlのversionは `v1.18.0`

#### secret.yamlの生成

```shell
$ cp kubernetes/base/secret_sample.yaml kubernetes/base/secret.yaml
# echo -n [value] | base64 でencode dataをenvfile.sampleに相当する値を生成する
$ [editor] kubernetes/base/secret.yaml
```

#### secret.yamlのdata/akashi_user_infoの更新

* akashi_user_infoはuser:tokenの組み合わせ(dict)になっている
* 以下のことを想定してツールを`/bin`配下に設置している
  1. 登録するユーザが増える
  1. 登録していたユーザを削除する
  1. 登録しているユーザのtokenを更新する(akashiのtokenは1ヶ月でexpireされる)
  1. etc...
* 各種ツールの使い方は `--help` で参照

  ```shell
  $ poetry run python bin/append_user.py --help
  usage: append_user.py [-h] -c CONFIG -n NAME -t TOKEN [-r]
  
  optional arguments:
    -h, --help            show this help message and exit
    -c CONFIG, --config CONFIG
                          k8sのsecret yamlのファイルパス
    -n NAME, --name NAME  追加するuser名
    -t TOKEN, --token TOKEN
                          userのtoken
    -r, --raw             user情報をjsonのまま出力する
  ```

#### Kubernetesへのデプロイ

```shell
$ kubectl kustomize kubernetes/base | kubectl apply -f -
```

#### Kubernetesのリソース削除

```shell
$ kubectl kustomize kubernetes/base | kubectl delete -f -
```

#### slackでの使い方

* botにメンションをつけて特定のmessageを付与する
* plugin.pyの `@respond_to` を編集することでmessageの編集ができる
* 以下はSlack内の例  
![出勤の例](/doc/img/shukkin.png)
  