# attendance-slack

* Slackのbot.
  * slackに特定のコメントが付くと, Akashiと連携して出退勤をする
* AkashiのAPIは以下
  * https://akashi.zendesk.com/hc/ja/sections/115000138574-%E5%85%AC%E9%96%8BAPI

# Usage
## setup
* pipenvのインストール
    * ref: https://github.com/pypa/pipenv
* libraryのインストール
    ```shell
    $ pipenv install
    ```
## 起動
* 設定ファイルの編集
    ```shell
    $ cp envfile.sample envfile
    # envfileはDokcer用の環境変数
    # localできどうするときはexportで設定するように修正する
    $ [editor] envfile
    ```

### docker
#### upload済みのdocker imageで起動
* dokcer hubにimageをアップロード済み
    https://hub.docker.com/repository/docker/yamamoi/attendance-slack
* 起動
    ```shelll
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
### local起動
* 起動
    ```shell
    $ source envfile_local
    $ python run.sh
    ```

# slackでの使い方

* botにメンションをつけて特定のmessageを付与する
* plugin.pyの `@respond_to` を編集することでmessageの編集ができる
* 以下はSlack内の例  
![出勤の例](/doc/img/shukkin.png)
