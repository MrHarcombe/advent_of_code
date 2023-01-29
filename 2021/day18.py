from itertools import permutations
import io


class SnailPair:
    def __init__(self, left, right):
        self.left = left
        self.right = right


    def __add__(self, other):
        return SnailPair(self, other).reduce()


    def __str__(self):
        output = ''
        if isinstance(self.left, list):
            output = f'[{self.left[0]},'
        else:
            output = '[' + str(self.left) + ','

        if isinstance(self.right, list):
            output += f'{self.right[0]}]'
        else:
            output += str(self.right) + ']'
        return output


    def __pre_order_find_explode(self, count=0):
        # if isinstance(self.left, SnailPair) and isinstance(self.right, SnailPair):
        #     # if count has got to 3, then this is the 4th
        #     if count >= 3:
        #         return self

        if isinstance(self.left, SnailPair):
            # if count has got to 3, then left will be the 4th
            if count >= 3:
                return self.left

            result = self.left.__pre_order_find_explode(count+1)
            if result:
                return result

        if isinstance(self.right, SnailPair):
            if count >= 3:
                return self.right

            result = self.right.__pre_order_find_explode(count+1)
            if result:
                return result

        if not (isinstance(self.left, SnailPair) and isinstance(self.right, SnailPair)):
            count = 0


    def __pre_order_find_split(self):
        if isinstance(self.left, list):
            if self.left[0] > 9:
                return self
        else:
            found = self.left.__pre_order_find_split()
            if found:
                return found

        if isinstance(self.right, list):
            if self.right[0] > 9:
                return self
        else:
            return self.right.__pre_order_find_split()


    def __in_order_build_list(self, inorder=[]):
        if self.left != None:
            if isinstance(self.left, SnailPair):
                self.left.__in_order_build_list(inorder)

        inorder.append(self)

        if self.right != None:
            if isinstance(self.right, SnailPair):
                self.right.__in_order_build_list(inorder)

        return inorder


    def reduce(self):
        # need to repeatedly:
        # - check for more than 4 nested numbers -> explode
        # - check for any individual number > 10 -> split

        did_something = True
        while did_something:
            did_something = False

            # explode the first pre-order traversal where you
            # can count exactly 4 SnailPair instances on the trot?
            boom = self.__pre_order_find_explode()
            if boom:
                did_something = True
                # print("boom:", boom)
                boom.explode(self)

            if not did_something:
                # split the first pre-order traversal where you
                # can find a number > 9?
                splot = self.__pre_order_find_split()
                if splot:
                    did_something = True
                    # print("splot:", splot)
                    splot.split()

            # print(self)

        return self


    def explode(self, start):
        value_left = self.left[0]
        value_right = self.right[0]

        inorder_nodes = start.__in_order_build_list([])
        replace = inorder_nodes.index(self)

        if replace > 0:
            if inorder_nodes[replace-1].right == self:
                inorder_nodes[replace-1].left[0] += value_left
            else:
                if isinstance(inorder_nodes[replace-1].left, list):
                    inorder_nodes[replace-1].left[0] += value_left
                else:
                    runner = inorder_nodes[replace-1].left
                    while isinstance(runner.right, SnailPair):
                        runner = runner.right
                    runner.right[0] += value_left

        if replace <= len(inorder_nodes)-2:
            if isinstance(inorder_nodes[replace+1].right, list):
                inorder_nodes[replace+1].right[0] += value_right
            else:
                runner = inorder_nodes[replace+1].right
                while isinstance(runner.left, SnailPair):
                    runner = runner.left
                runner.left[0] += value_right

        for node in inorder_nodes:
            if node.left and node.left == self:
                node.left = [0]
            elif node.right and node.right == self:
                node.right = [0]


    def split(self):
        if isinstance(self.left, list) and self.left[0] > 9:
            self.left = SnailPair([self.left[0] // 2], [(self.left[0] // 2) + (self.left[0] % 2)])
        else:
            self.right = SnailPair([self.right[0] // 2], [(self.right[0] // 2) + (self.right[0] % 2)])


    def magnitude(self):
        mag = 0
        if isinstance(self.left, list):
            mag += 3 * self.left[0]
        else:
            mag += 3 * self.left.magnitude()

        if isinstance(self.right, list):
            mag += 2 * self.right[0]
        else:
            mag += 2 * self.right.magnitude()

        return mag


def parse_snail_number(line):
    if line.isdigit():
        return [int(line)]

    else:
        consider = line[1:-1]
        if '[' not in consider:
            left, right = [[int(n)] for n in consider.split(',')]
            return SnailPair(left, right)

        else:
            open = 0
            for i, ch in enumerate(consider):
                if ch == '[':
                    open += 1
                elif ch == ']':
                    open -= 1
                elif ch == ',' and open == 0:
                    break
            left = parse_snail_number(consider[:i])
            right = parse_snail_number(consider[i+1:])
            return SnailPair(left, right)

test_1 = '''[1,2]
[[3,4],5]'''
test_2 = '''[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]'''
test_3 = '''[[[[[9,8],1],2],3],4]'''
test_4 = '''[7,[6,[5,[4,[3,2]]]]]'''
test_5 = '''[[6,[5,[4,[3,2]]]],1]'''
test_6 = '''[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]'''
test_7 = '''[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]'''
test_8 = '''[[[[4,3],4],4],[7,[[8,4],9]]]
[1,1]'''
test_9 = '''[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]'''
test_10 = '[9,1]'
test_11 = '[[1,2],[[3,4],5]]'
test_12 = '[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]'
test_12b = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''
test_13 = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''

test = test_13

numbers = []
with io.StringIO(test) as inputs:
# with open('input18.txt') as inputs:
    for line in inputs:
        numbers.append(parse_snail_number(line.strip()))

total = numbers[0]
print(total)
for number in numbers[1:]:
    total += number
print(total)
print(total.magnitude())
print()

numbers = []
# with io.StringIO(test) as inputs:
with open('input18.txt') as inputs:
    for line in inputs:
        numbers.append(line.strip())

maxima = []
for first, second in permutations(numbers, 2):
    # print(first,second)
    answer = parse_snail_number(first) + parse_snail_number(second)
    # print('answer:', answer)
    mag = answer.magnitude()
    # print('magnitude:', mag)
    maxima.append((mag, (str(answer),'->',str(first),str(second))))

# print(maxima)
print(max(maxima))