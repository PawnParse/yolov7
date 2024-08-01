python train.py \
    --workers 8 \
    --device 0 \
    --batch-size 24 \
    --data data/bbox5.yaml \
    --img 1280 1280 \
    --cfg cfg/training/yolov7-tiny.yaml \
    --weights 'yolov7-tiny.pt' \
    --name yolov7-bbox5-tiny \
    --hyp data/hyp.chess.tiny.yaml