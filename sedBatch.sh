while read line; do 
    sed -i 's/immuneportal_django_app/immuneportal_django_app/g' $line
done < out.txt
