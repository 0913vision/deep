for((i=3;i<=7;i++)); do
    cp ./hosts$((i-1)) ./hosts$i
    echo "remote$i slots=1" >> ./hosts$i
done