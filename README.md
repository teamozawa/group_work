# 使い方
※このモデルラズベリーパイの使用を前提としています。

## 事前準備
https://qiita.com/TEAM_OZAWA/items/f630fefbf92289eae39b
- 上記ののURLに掲載されているコードを実装し、predict_modelを"eff3_model.h5"というファイル名で保存します。
- 同じく、hold_vectorを"hold_vector.npy"というファイル名で保存します。
- このディレクトリをクローンします。
```
git clone https://github.com/teamozawa/group_work.git
```
- 保存済みの重みを```models```にコピーします。
```
cp PATH/eff3_model.h5 PATH/group_work/models
```
- 保存済みのデータファイルを```models```にコピーします。
```
cp PATH/hold_vector.npy PATH/group_work/models
```
