from itertools import chain
from save_to_db.core.exceptions import ItemsNotTheSame


def merge_items(items, all_items):
    """ Merges items that pull the same model from the database into a single
    items.
    
    :param items: List of items in which items referring to the same model
        must be merged.
    """
    merged_items = []
    
    while True:
        for item in items:
            item_merged = False
            
            if item in merged_items or not item.getters:
                continue
            
            for group in item.getters:
                
                use_group = True
                for field_name in group:
                    if field_name not in item.data:
                        use_group = False
                        break  
                if not use_group:
                    continue
                
                for next_item in items:
                    if next_item is item or next_item in merged_items:
                        continue
                    
                    do_merge = True
                    for key in group:
                        
                        if key not in next_item or \
                                next_item[key] != item[key]:
                            do_merge = False
                            break
                    if not do_merge:
                        continue
                            
                    __merge_item_into_item(item, next_item)
                    merged_items.append(next_item)
                    item_merged = True
            
            if item_merged:
                break
        
        # replacing merged_items with the extended item
        for merged_item in merged_items:
            for one_item in all_items:
                for key, value in one_item.data.items():
                    if value is merged_item:
                        one_item[key] = item
            
            items.remove(merged_item)
        merged_items.clear()
        
        if not item_merged:
            break
        


def __same_items(item_one, item_two):
    for key in set(chain(item_one.data.keys(), item_two.data.keys())):
        if key not in item_one.data or key not in item_two.data:
            continue
        
        if key in item_one.relations and \
                item_one.relations[key]['relation_type'].is_x_to_many():
            continue
        
        if key not in item_one.data or key not in item_two.data or \
                item_two.data[key] != item_one.data[key]:
            return False
        
    return True


def __merge_item_into_item(extended_item, merged_item):
    if not __same_items(extended_item, merged_item):
        raise ItemsNotTheSame(extended_item, merged_item)
    
    for key in merged_item.data:
        is_x_to_many = False
        if key in extended_item.relations:
            is_x_to_many = \
                extended_item.relations[key]['relation_type'].is_x_to_many()
        
        if not is_x_to_many:
            if key not in extended_item.data:
                extended_item[key] = merged_item[key]
        else:
            for item in merged_item[key].bulk:
                extended_item[key].add(item)
                
                