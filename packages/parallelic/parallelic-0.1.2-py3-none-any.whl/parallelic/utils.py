def args_to_kv(*args):
    print(args)
    return {args[i]: args[i+1] for i in range(0, len(args), 2)}
