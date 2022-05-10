TEXT=data/028
fairseq-preprocess --source-lang en --target-lang de     --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test     --destdir bin/028     --workers 20