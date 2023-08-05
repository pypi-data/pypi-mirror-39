def parse_mongo_dict(args):
    """
    :return:
    """

    mongo_dict = dict()

    # iterate through --mdata and split it to dict
    for mdata in args.mongo_dict:
        temp_val = mdata.split("=")

        my_list = []
        for k in temp_val[1].split(","):
            my_list.append(k)

        mongo_dict[my_list[0]] = my_list[1:]

    return mongo_dict
