import sys
from organize.balanceConstants import BalanceConstants
from organize.balanceTree import BalanceTree

class Balancer(object):
    def __init__(self, tree_values):
        self.files_to_exclude = ({
            'Backups.backupdb'
        })
        self.tree_values = tree_values
        self.trees = []
        self._constants = BalanceConstants()

    def _create_trees(self):
        self.trees = [BalanceTree(value[self._constants.disk_path], value[self._constants.root_path])
                      for value in self.tree_values]
        return None

    def balance(self):
        self._create_trees()
        while self._continue_balancing():
            to_index = self._move_tree_index(True)
            from_index = self._move_tree_index(False)
            to_tree = self.trees[to_index]
            from_tree = self.trees[from_index]
            print('from index:', from_index, 'moving from:', from_tree.root_path, 'with used space:', from_tree.used_space)
            print('to index:', to_index, 'moving to:', to_tree.root_path, 'with used space:', to_tree.used_space)
            if from_index > to_index:
                lower_index = to_index
                upper_index = from_index
                move_lower = True
            else:
                lower_index = from_index
                upper_index = to_index
                move_lower = False
            self._move_alphabetical(lower_index, upper_index, move_lower)
        return None

    def _move_alphabetical(self, lower_index, upper_index, move_lower=True):
        if move_lower:
            from_index = upper_index
            to_index = lower_index
        else:
            from_index = lower_index
            to_index = upper_index
        keep_moving = True
        while keep_moving:
            from_tree = self.trees[from_index]
            to_tree = self.trees[to_index]
            if move_lower:
                balance_file = from_tree.pop_first_file()
                from_index += 1
            else:
                balance_file = from_tree.pop_last_file()
                to_index -= 1
            to_tree.add_file(balance_file)
            if from_index == to_index:
                keep_moving = False
        return None

    def _move_tree_index(self, move_to):
        target = 0
        free_space = 0
        if not move_to:
            free_space = sys.maxsize
        for i in range(len(self.trees)):
            tree = self.trees[i]
            tree_free_space = tree.free_space()
            if (move_to and tree_free_space > free_space) or \
                    (not move_to and tree_free_space < free_space):
                free_space = tree_free_space
                target = i
        return target

    def _continue_balancing(self):
        cont = False
        for i in range(len(self.trees) - 1):
            tree1 = self.trees[i]
            tree2 = self.trees[i + 1]
            file1 = tree1.last_file()
            file2 = tree2.first_file()
            if file2.name < file1.name:
                cont = True
                break
        return cont

    def _keep_balancing(self, to_tree, balance_file):
        return None

    def _add_slash_to_dir(self, dir):
        if dir[len(dir) - 1] != '/':
            dir += '/'
        return dir
