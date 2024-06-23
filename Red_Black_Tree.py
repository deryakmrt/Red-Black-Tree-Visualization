import sys
from typing import Type, TypeVar, Iterator
import networkx as nx
import matplotlib.pyplot as plt
#21100011001 - DERYA NAİLİYE KIMIRTI
# Uygulamanın test ve görselleştirme aşaması--> kodun en sonunda 445. satırdan itibaren
# T, Node sınıfından türeyen sınıfları temsil eden bir tür değişkeni
T = TypeVar('T', bound='Node')

# Node oluşturma
class Node():
    def __init__(self: T, key: int) -> None:
        self._key = key  # Düğümün anahtarı
        self.parent = None  # Ebeveyn düğüm
        self.left = None  # Sol çocuk düğüm
        self.right = None  # Sağ çocuk düğüm
        self._color = 1 # 1 -> KIRMIZI, 0 -> SIYAH (Renk)
        self.value = None  # Düğümün değeri

    def __repr__(self: T) -> str:
        return "Key: " + str(self._key) + " Value: " + str(self.value)  # Düğümün temsilini döndürür

    def get_color(self: T) -> str:
        return "black" if self._color == 0 else "red"  # Düğümün rengini döndürür

    def set_color(self: T, color: str) -> None:
        if color == "black":
            self._color = 0  # Düğümün rengini siyah yapar
        elif color == "red":
            self._color = 1  # Düğümün rengini kırmızı yapar
        else:
            raise Exception("Unknown color")  # Geçersiz renk girildiğinde hata fırlatır

    def get_key(self: T) -> int:
        return self._key  # Düğümün anahtarını döndürür

    def is_red(self: T) -> bool:
        return self._color == 1  # Düğümün kırmızı olup olmadığını kontrol eder

    def is_black(self: T) -> bool:
        return self._color == 0  # Düğümün siyah olup olmadığını kontrol eder

    def is_null(self: T) -> bool:
        return self._key is None  # Düğümün boş olup olmadığını kontrol eder

    def depth(self: T) -> int:
        return 0 if self.parent is None else self.parent.depth() + 1  # Düğümün derinliğini hesaplar

    @classmethod
    def null(cls: Type[T]) -> T:
        node = cls(0)  # Null düğüm oluşturur
        node._key = None  # Null düğümün anahtarını None yapar
        node.set_color("black")  # Null düğümün rengini siyah yapar
        return node  # Null düğümü döndürür


# RedBlackTree sınıfından türeyen sınıfları temsil eden bir tür değişkeni
T = TypeVar('T', bound='RedBlackTree')

class RedBlackTree():
    def __init__(self: T) -> None:
        self.TNULL = Node.null()  # Null düğüm oluşturur
        self.root = self.TNULL  # Ağacın kökünü null düğüm olarak ayarlar
        self.size = 0  # Ağacın başlangıç boyutu 0
        self._iter_format = 0  # İterasyon formatı (0: öncelik, 1: içsel, 2: sonrası)

    # Dunder Methods #
    def __iter__(self: T) -> Iterator:
        if self._iter_format == 0:
            return iter(self.preorder())  # Öncelik sıralamasında iterasyon
        if self._iter_format == 1:
            return iter(self.inorder())  # İçsel sıralamada iterasyon
        if self._iter_format == 2:
            return iter(self.postorder())  # Sonrası sıralamada iterasyon

    def __getitem__(self: T, key: int) -> int:
        return self.search(key).value  # Belirli bir anahtarla düğümün değerini döndürür

    def __setitem__(self: T, key: int, value: int) -> None:
        self.search(key).value = value  # Belirli bir anahtarla düğümün değerini ayarlar

    # Setters and Getters #
    def get_root(self: T) -> Node:
        return self.root  # Ağacın kökünü döndürür

    def set_iteration_style(self: T, style: str) -> None:
        if style == "pre":
            self._iter_format = 0  # İterasyon formatını öncelik sıralaması yapar
        elif style == "in":
            self._iter_format = 1  # İterasyon formatını içsel sıralama yapar
        elif style == "post":
            self._iter_format = 2  # İterasyon formatını sonrası sıralama yapar
        else:
            raise Exception("Unknown style.")  # Geçersiz stil girildiğinde hata fırlatır

    # Iterators #
    def preorder(self: T) -> list:
        return self.pre_order_helper(self.root)  # Öncelik sıralamasında düğümleri döndürür

    def inorder(self: T) -> list:
        return self.in_order_helper(self.root)  # İçsel sıralamada düğümleri döndürür

    def postorder(self: T) -> list:
        return self.post_order_helper(self.root)  # Sonrası sıralamada düğümleri döndürür

    def pre_order_helper(self: T, node: Node) -> list:
        """
        Belirtilen düğümden başlayarak öncelik sıralamasında ağaç dolaşımı gerçekleştirir.
        """
        output = []
        if not node.is_null():
            left = self.pre_order_helper(node.left)  # Sol alt ağacı dolaş
            right = self.pre_order_helper(node.right)  # Sağ alt ağacı dolaş
            output.extend([node])  # Düğümü ekle
            output.extend(left)  # Sol alt ağacın düğümlerini ekle
            output.extend(right)  # Sağ alt ağacın düğümlerini ekle
        return output

    def in_order_helper(self: T, node: Node) -> list:
        """
        Belirtilen düğümden başlayarak içsel sıralamada ağaç dolaşımı gerçekleştirir.
        """
        output = []
        if not node.is_null():
            left = self.in_order_helper(node.left)  # Sol alt ağacı dolaş
            right = self.in_order_helper(node.right)  # Sağ alt ağacı dolaş
            output.extend(left)  # Sol alt ağacın düğümlerini ekle
            output.extend([node])  # Düğümü ekle
            output.extend(right)  # Sağ alt ağacın düğümlerini ekle
        return output

    def post_order_helper(self: T, node: Node) -> list:
        output = []
        if not node.is_null():
            left = self.post_order_helper(node.left)  # Sol alt ağacı dolaş
            right = self.post_order_helper(node.right)  # Sağ alt ağacı dolaş
            output.extend(left)  # Sol alt ağacın düğümlerini ekle
            output.extend(right)  # Sağ alt ağacın düğümlerini ekle
            output.extend([node])  # Düğümü ekle
        return output

    # Ağacı arar
    def search_tree_helper(self: T, node: Node, key: int) -> Node:
        if node.is_null() or key == node.get_key():
            return node  # Anahtar düğümü bulur veya null düğüm döner

        if key < node.get_key():
            return self.search_tree_helper(node.left, key)  # Sol alt ağacı arar
        return self.search_tree_helper(node.right, key)  # Sağ alt ağacı arar

    # Silme işleminden sonra ağacı dengeleme
    def delete_fix(self: T, x: Node) -> None:
        while x != self.root and x.is_black():
            if x == x.parent.left:
                s = x.parent.right
                if s.is_red():
                    s.set_color("black")
                    x.parent.set_color("red")
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.is_black() and s.right.is_black():
                    s.set_color("red")
                    x = x.parent
                else:
                    if s.right.is_black():
                        s.left.set_color("black")
                        s.set_color("red")
                        self.right_rotate(s)
                        s = x.parent.right

                    s.set_color(x.parent.get_color())
                    x.parent.set_color("black")
                    s.right.set_color("black")
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.is_red():
                    s.set_color("black")
                    x.parent.set_color("red")
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.is_black() and s.right.is_black():
                    s.set_color("red")
                    x = x.parent
                else:
                    if s.left.is_black():
                        s.right.set_color("black")
                        s.set_color("red")
                        self.left_rotate(s)
                        s = x.parent.left

                    s.set_color(x.parent.get_color())
                    x.parent.set_color("black")
                    s.left.set_color("black")
                    self.right_rotate(x.parent)
                    x = self.root
        x.set_color("black")

    def __rb_transplant(self: T, u: Node, v: Node) -> None:
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    # Düğüm silme
    def delete_node_helper(self: T, node: Node, key: int) -> None:
        z = self.TNULL
        while not node.is_null():
            if node.get_key() == key:
                z = node

            if node.get_key() <= key:
                node = node.right
            else:
                node = node.left

        if z.is_null():
            # Anahtarı ağaçta bulamıyorsa
            return

        y = z
        y_original_color = y.get_color()
        if z.left.is_null():
            # Sol çocuk yoksa, sağ alt ağacı yukarı kaydır
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right.is_null()):
            # Sağ çocuk yoksa, sol alt ağacı yukarı kaydır
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.get_color()
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.set_color(z.get_color())
        if y_original_color == "black":
            self.delete_fix(x)

        self.size -= 1

    # Ekleme işleminden sonra ağacı dengeleme
    def fix_insert(self: T, node: Node) -> None:
        while node.parent.is_red():
            if node.parent == node.parent.parent.right:
                u = node.parent.parent.left
                if u.is_red():
                    u.set_color("black")
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    node = node.parent.parent
                else:
                    if node == node.parent.left:
                        node = node.parent
                        self.right_rotate(node)
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    self.left_rotate(node.parent.parent)
            else:
                u = node.parent.parent.right

                if u.is_red():
                    u.set_color("black")
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    node = node.parent.parent
                else:
                    if node == node.parent.right:
                        node = node.parent
                        self.left_rotate(node)
                    node.parent.set_color("black")
                    node.parent.parent.set_color("red")
                    self.right_rotate(node.parent.parent)
            if node == self.root:
                break
        self.root.set_color("black")

    # Ağacı yazdırma
    def __print_helper(self: T, node: Node, indent: str, last: bool) -> None:
        if not node.is_null():
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----  ")
                indent += "     "
            else:
                sys.stdout.write("L----   ")
                indent += "|    "

            s_color = "RED" if node.is_red() else "BLACK"
            print(str(node.get_key()) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def search(self: T, key: int) -> Node:
        return self.search_tree_helper(self.root, key)  # Anahtarı arar ve düğümü döndürür

    def minimum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node.is_null():
            return self.TNULL
        while not node.left.is_null():
            node = node.left
        return node  # En küçük anahtarı bulur ve düğümü döndürür

    def maximum(self: T, node: Node = None) -> Node:
        if node is None:
            node = self.root
        if node.is_null():
            return self.TNULL
        while not node.right.is_null():
            node = node.right
        return node  # En büyük anahtarı bulur ve düğümü döndürür

    def successor(self: T, x: Node) -> Node:
        if not x.right.is_null():
            return self.minimum(x.right)  # Ardışık düğümü bulur ve döndürür

        y = x.parent
        while not y.is_null() and x == y.right:
            x = y
            y = y.parent
        return y  # Ardışık düğümü döndürür

    def predecessor(self: T, x: Node) -> Node:
        if (not x.left.is_null()):
            return self.maximum(x.left)  # Önceki düğümü bulur ve döndürür

        y = x.parent
        while not y.is_null() and x == y.left:
            x = y
            y = y.parent

        return y  # Önceki düğümü döndürür

    def left_rotate(self: T, x: Node) -> None:
        y = x.right
        x.right = y.left
        if not y.left.is_null():
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y  # Sol rotasyon yapar

    def right_rotate(self: T, x: Node) -> None:
        y = x.left
        x.left = y.right
        if not y.right.is_null():
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y  # Sağ rotasyon yapar

    def insert(self: T, key: int) -> None:
        node = Node(key)
        node.left = self.TNULL
        node.right = self.TNULL
        node.set_color("red")

        y = None
        x = self.root

        while not x.is_null():
            y = x
            if node.get_key() < x.get_key():
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.get_key() < y.get_key():
            y.left = node
        else:
            y.right = node

        self.size += 1

        if node.parent is None:
            node.set_color("black")
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def delete(self: T, key: int) -> None:
        self.delete_node_helper(self.root, key)

    def print_tree(self: T) -> None:
        self.__print_helper(self.root, "", True)

    def visualize_tree(self: T) -> None:
        G = nx.DiGraph()

        def add_edges(node):
            if not node.is_null():
                if not node.left.is_null():
                    G.add_edge(node.get_key(), node.left.get_key(), color=node.left.get_color())
                    add_edges(node.left)
                if not node.right.is_null():
                    G.add_edge(node.get_key(), node.right.get_key(), color=node.right.get_color())
                    add_edges(node.right)

        add_edges(self.root)

        pos = nx.spring_layout(G)
        colors = [G[u][v]['color'] for u, v in G.edges]
        nx.draw(G, pos, edge_color=colors, with_labels=True, node_size=700, node_color="white", font_weight="bold",
                font_color="black")
        plt.show()

#-----------------------------------------------------------------------------------
# RedBlackTree sınıfını görselleştirme ile test et

if __name__ == "__main__":
    rbt = RedBlackTree()

    # Elemanları ekle
    elements = [20, 15, 25, 10, 5, 1, 30, 35, 50]
    for element in elements:
        rbt.insert(element)

    # Ağacı yazdır
    print("Elemanlar eklendikten sonra ağaç:")
    rbt.print_tree()

    # Ağacı görselleştir
    rbt.visualize_tree()

    # Bir düğümü sil
    rbt.delete(10)

    # Silme işleminden sonra ağacı yazdır
    print("\n10 silindikten sonra ağaç:")
    rbt.print_tree()

    # Silme işleminden sonra ağacı görselleştir
    rbt.visualize_tree()

    # Başka bir düğümü sil
    rbt.delete(20)

    # Başka bir silme işleminden sonra ağacı yazdır
    print("\n20 silindikten sonra ağaç:")
    rbt.print_tree()

    # agaci görselleştir
    rbt.visualize_tree()