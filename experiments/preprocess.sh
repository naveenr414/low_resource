TEXT=data/005
fairseq-preprocess --source-lang en --target-lang de     --trainpref $TEXT/train --validpref $TEXT/valid --testpref $TEXT/test     --destdir bin/005     --workers 20