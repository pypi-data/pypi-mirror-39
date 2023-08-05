
        >>> from torchvision.models import densenet
        >>> initkw = {'growth_rate': 16}
        >>> model = densenet.DenseNet(**initkw)
        >>> export_model_code('./somefolder', model, initkw)
        ./somefolder/DenseNet_c662ba.py

