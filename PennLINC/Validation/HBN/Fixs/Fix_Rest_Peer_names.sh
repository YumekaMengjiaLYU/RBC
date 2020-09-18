
datain=''

for i in $(find $datain -iname '*run-1_run-01*');do
    i_new2=${i/run-1_run-01/run-1_run-02}
    if [[ -f $i_new2 ]];then
        rm $i
        i_new3=${i/run-1_run-01/run-1_run-03}
        if [[ -f $i_new3 ]];then
            rm $i_new2
            i_new=${i_new3/run-1_run-03/run-1}
            mv $i_new3 $i_new
        else
            i_new=${i_new2/run-1_run-02/run-1}
            mv $i_new2 $i_new
        fi
    fi
done



for i in $(find $datain -iname '*run-2_run-01*');do
    i_new2=${i/run-2_run-01/run-2_run-02}
    if [[ -f $i_new2 ]];then
        rm $i
        i_new3=${i/run-2_run-01/run-2_run-03}
        if [[ -f $i_new3 ]];then
            rm $i_new2
            i_new=${i_new3/run-2_run-03/run-2}
            mv $i_new3 $i_new
        else
            i_new=${i_new2/run-2_run-02/run-2}
            mv $i_new2 $i_new
        fi
    fi
done


for i in $(find $datain -iname '*run-3_run-01*');do
    i_new2=${i/run-3_run-01/run-3_run-02}
    if [[ -f $i_new2 ]];then
        rm $i
        i_new3=${i/run-3_run-01/run-3_run-03}
        if [[ -f $i_new3 ]];then
            rm $i_new2
            i_new=${i_new3/run-3_run-03/run-3}
            mv $i_new3 $i_new
        else
            i_new=${i_new2/run-3_run-02/run-3}
            mv $i_new2 $i_new
        fi
    fi
done
