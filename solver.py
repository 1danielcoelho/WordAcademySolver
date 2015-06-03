__author__ = 'Mariana'

import argparse

class Node:
    def __init__(self):
        self.nodes = []
        self.letra = ''
        self.index = 0

class Graph:
    def __init__(self, wordlist):
        self.node_list = []
        self.letters = ""
        self.rows = 0
        self.cols = 0

    def createGrid(self, rows, cols, letters):
        """
        Creates a set of Nodes properly connected, according to letters, in a rows x cols grid
        :param rows: Integer larger than zero. Number of rows of the grid (even if no tiles are present on every spot)
        :param cols: Integer larger than zero. Number of cols of the grid (even if no tiles are present on every spot)
        :param letters: String with rows*cols characters. Use "-" to indicate an empty tile. Example:
                        "--------a---bcde"
        :return: Nothing
        """

        self.letters = letters
        self.rows = rows
        self.cols = cols

        # creates our node list of desired size
        self.node_list = [Node() for _ in range(rows*cols)]

        # adds the letters to each node
        for index, node in enumerate(self.node_list):
            node.letra = letters[index]
            node.index = index

        for y in range(rows):
            for x in range(cols):

                index = x + y*rows

                for delta_x in range(-1, 2):
                    for delta_y in range(-1, 2):
                        new_x = x + delta_x
                        new_y = y + delta_y
                        new_index = new_x + new_y*rows

                        if new_x < 0 or new_x > cols-1 or new_y < 0 or new_y > rows-1 or new_index is index:
                            continue

                        elif self.letters[new_index] != '-':
                            self.node_list[index].nodes.append(self.node_list[new_index])

    def __str__(self):
        result = "Current grid: \n"

        for row in range(self.rows):
            result += self.letters[row*self.cols:row*self.cols+self.cols] + "\n"

        return result

    def searchWords(self, length, wordlist):
        """
        Searches words of argument length in the grid. Returns found words that are also in argument wordlist
        :param length: Integer larger than zero. Number of characters of the words to search
        :param wordlist: List of strings, where each is a valid word
        :return: List of strings containing words found in the grid that are also present in the wordlist
        """

        # Grab only the words from the wordlist that fit the number of characters
        wordlist_small = []
        for word in wordlist:
            if len(word) is length:
                wordlist_small.append(word)

        print "Database holds " + str(len(wordlist_small)) + " words with length " + str(length) + "."

        words = []

        for node in self.node_list:
            if self.letters[node.index] != '-':
                used = [False] * self.rows * self.cols
                used[node.index] = True
                self.findAllWords(node, "", words, length-1, used, wordlist_small)

        print "Found " + str(len(words)) + " word(s) with length " + str(length) + " in this grid:"

        for word in words:
            print "\t" + word

    def findAllWords(self, node, current_word, words, length_left, used, wordlist):
        """
        Recursively finds all the valid words starting at node, that have length_left characters (not including the
        currently observed node)
        :param node: Node currently being observed
        :param current_word: String containing the current word being formed as we travel through the nodes
        :param words: Big list of all words already found. All of those were already checked to be present in wordlist
        :param length_left: Number of characters still missing until current_word becomes the target length
        :param used: Array of rows*cols elements used to track which Nodes have already been used in the current word
        :param wordlist: Large list of strings containing all valid words
        :return: Nothing
        """
        current_word += node.letra

        # Return early in case we're following a dead end
        for word in wordlist:
            if current_word in word:
                break
        else:
            return

        if length_left is 0:
            if current_word in wordlist and current_word not in words:
                words.append(current_word)
            else:
                return

        for other_node in node.nodes:
            if used[other_node.index]:
                continue

            used[other_node.index] = True
            self.findAllWords(other_node, current_word, words, length_left-1, used, wordlist)
            # We already explored all words with node->other_node, but other_node may belong to another word starting
            # elsewhere
            used[other_node.index] = False


def main():
    parser = argparse.ArgumentParser(description='Solves a WordAcademy puzzle using a list of valid words')

    parser.add_argument('rows', help="Total number of rows of the playing field (includes empty spaces)", type=int)
    parser.add_argument('cols', help="Total number of columns of the playing field (includes empty spaces)", type=int)
    parser.add_argument('board', help="String of rows*cols characters indicating the playing field row by row. \
                                           Empty spaces should be indicated with a dash (-)")
    parser.add_argument('chars', help="Number of characters of the target word", type=int)
    parser.add_argument('-p', '--path', help="Path to the text file containing all valid words, one per line")

    args = parser.parse_args()

    # Only move forward if the number of rows, columns and the board itself all agree with eachother
    if len(args.board) != args.rows * args.cols:
        print "Error: Input board is " + str(len(args.board)) + " characters long, which differs from rows*cols = " + \
              str(args.rows * args.cols) + "."
        return 1

    print "Rows: " + str(args.rows) + ", cols: " + str(args.cols)

    if args.path is None:
        args.path = r"C:\Users\1dani_000\Dropbox\Python\Projects\Wordacademy\palavras.txt"

    with open(args.path, "r") as input_file:
        words = []
        for line in input_file:
            words.append(line[:line.find("-")].lower())

    grid = Graph(words)
    grid.createGrid(args.rows, args.cols, args.board)
    print grid

    print "Target word is " + str(args.chars) + " characters long."
    grid.searchWords(args.chars, words)



if __name__ == "__main__":
    main()
