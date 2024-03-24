#!/usr/bin/awk -f

BEGIN{
    print "Start";
    FS = "        ";
}
{
    if(NR >= 10){
        m = substr($1, 5);
        s = substr($2, 5); 
        a = $3;
        b = $4;
        if(m != s){
            print m " " s;
        }
    }
}

END{
    print "Done";
}
