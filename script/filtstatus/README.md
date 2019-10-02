# FiltStatus

* check\_epics\_gwf.py
	* 指定したStart時刻でのSWSTATの値を呼んで、フィルターの何が押されているか表示するスクリプト。
* check\_epics\_ezca.py
	* EZCA で現在のチャンネルを読む Version。あまり使わない。
* main.job
	* Condor で動かすためのジョブファイル。
* swstat.txt
	* 調べたいフィルターを与えるカード。
* results
	* 出力結果。

## 使い方
1. check\_epics\_gwf.py に知りたい時刻と、その名前を追加
2. ジョブファイルに	その名前を書く。
3. ジョブを投下

## 出力結果の読み方

例) 
> "Filter Name" | Gain,Offset,Limit,"STATUS", "Filter Number"

1. K1:VIS-ETMX\_KALMAN\_KEST\_X2\_SWSTAT                 : ('DEFAULT\_OUT', [])
2. K1:VIS-ETMX\_IP\_COILOUTF\_H1\_SWSTAT                 : ('LIMIT\_OUT', [1, 2, 3, 6, 7, 8])
3. K1:VIS-ETMX\_IP\_TEST\_L\_SWSTAT                      : ('OFFSET\_OUT', [])
4. K1:VIS-ETMX\_IP\_SEISFF\_L\_SWSTAT                    : ('NO\_OUT', [4, 7, 10])
5. K1:VIS-ETMX\_PAY\_OLSERVO\_DAMP\_P19\_SWSTAT          : 0,b,1,1,0,1,1,0,1,0,0,1,0,1,0,0,1,0,1


* STATUSの意味
	* DEFAULT\_OUT | IN1,OUT,DEC がONで、信号が出力されている状態。
	* LIMIT\_OUT | DEFAULT\_OUTにLIMITが追加。
	* OFFSET\_OUT | DEFAULT\_OUTにOFFSET\_OUTが追加。 
	* NO\_OUT | OUTがOFF。つまり出力がない。
	* binary | 上記以外の状態。直接バイナリを呼んで解読する必要あり。
* Filter Number の意味
	* FM1,FM2,FM3,FM4,FM5,FM6,FM7,FM8,FM9,FM10


| Button Name | bit |
|---|---|
|FM1  |  0|
|FM2  |  1|
|FM3  |  2|
|FM4  |  3|
|FM5  |  4|
|FM6  |  5|
|FM7  |  6|
|FM8  |  7|
|FM9  |  8|
|FM10 |  9|
|IN1  | 10|
|OSET | 11|
|OUT  | 12|
|LIM  | 13|
|DEC  | 15|
|HOLD | 16|

