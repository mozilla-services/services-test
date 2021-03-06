class Test_Open_Graph_Standards:

    def test_open_graph_present_tags(self, meta, url, required_tags, found_tags):
        og_assert = True

        # Test url and add found tags to list
        for req_tags in required_tags:
            for item in meta:
                if item.get('name') == req_tags or item.get('property') == req_tags:
                    found_tags.append(req_tags)
                else:
                    continue
            # Test found tags against required
            if req_tags in found_tags:
                continue
            else:
                print("Within url {0}: Item {1} not found".format(url, req_tags))
                og_assert = False
        assert og_assert
