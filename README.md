# 使い方
※このモデルはラズベリーパイの使用を前提としています。

https://qiita.com/TEAM_OZAWA/items/f630fefbf92289eae39b
- 上記のURLに掲載されているコードを実装し、predict_modelを```eff3_model.h5```というファイル名で保存します。
- 同じく、hold_vectorを```hold_vector.npy```というファイル名で保存します。
- このディレクトリをクローンします。
```
git clone https://github.com/teamozawa/group_work.git
```
- 保存済みのpredict_modelを```models```フォルダにコピーします。
```
cp PATH/eff3_model.h5 PATH/group_work/models
```
- 保存済みのhold_vectorを```models```フォルダにコピーします。
```
cp PATH/hold_vector.npy PATH/group_work/models
```
- ```group_work```ディレクトリに移動します。
```
cd PATH/group_work/
```
- ```main.py```を実行します。
```
python main.py
```
- 以降は画面の指示に従って実行してください
