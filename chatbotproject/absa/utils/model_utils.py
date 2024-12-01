import torch

def device_setting():
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")
    return device


def load_model(model, state_dict_path, device):
    current_model_dict = model.state_dict()
    loaded_state_dict = torch.load(state_dict_path, map_location=device)
    new_state_dict = {k: v if v.size() == current_model_dict[k].size() else current_model_dict[k] for k, v in
                      zip(current_model_dict.keys(), loaded_state_dict.values())}
    model.load_state_dict(new_state_dict, strict=False)
    model.to(device)

    return model