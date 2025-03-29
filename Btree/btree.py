class BTreeNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
    
    def __str__(self):
        return f"Keys: {self.keys}, Leaf: {self.leaf}"

class BTree:
    def __init__(self, order):
        if order < 3:
            raise ValueError("El orden del árbol B debe ser al menos 3")
        self.root = BTreeNode(leaf=True)
        self.order = order  # Máximo número de hijos
        self.min_keys = (order - 1) // 2  # Mínimo de claves en nodos no raíz
    
    def search(self, key, node=None):
        if node is None:
            node = self.root
        
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        
        if i < len(node.keys) and key == node.keys[i]:
            return (node, i)  # Encontrado
        elif node.leaf:
            return None  # No encontrado
        else:
            return self.search(key, node.children[i])
    
    def insert(self, key):
        root = self.root
        if len(root.keys) == (2 * self.min_keys + 1):
            new_root = BTreeNode()
            self.root = new_root
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)
    
    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.min_keys + 1):
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)
    
    def _split_child(self, parent, index):
        order = self.order
        child = parent.children[index]
        new_node = BTreeNode(leaf=child.leaf)
        
        # Mover las claves e hijos al nuevo nodo
        mid_key = child.keys[self.min_keys]
        new_node.keys = child.keys[self.min_keys + 1 : 2 * self.min_keys + 1]
        child.keys = child.keys[:self.min_keys]
        
        if not child.leaf:
            new_node.children = child.children[self.min_keys + 1 : 2 * self.min_keys + 2]
            child.children = child.children[:self.min_keys + 1]
        
        # Insertar la clave media en el padre
        parent.keys.insert(index, mid_key)
        parent.children.insert(index + 1, new_node)
    
    def delete(self, key):
        self._delete(self.root, key)
        # Si la raíz queda sin claves pero tiene un hijo, hacerlo la nueva raíz
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]
    
    def _delete(self, node, key):
        order = self.order
        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1
        
        # Caso 1: La clave está en el nodo actual y es hoja
        if idx < len(node.keys) and key == node.keys[idx] and node.leaf:
            node.keys.pop(idx)
            return
        
        # Caso 2: La clave está en el nodo actual y no es hoja
        if idx < len(node.keys) and key == node.keys[idx]:
            # Caso 2a: El hijo anterior tiene al menos min_keys + 1 claves
            if len(node.children[idx].keys) > self.min_keys:
                predecessor = self._get_predecessor(node.children[idx])
                node.keys[idx] = predecessor
                self._delete(node.children[idx], predecessor)
            # Caso 2b: El hijo siguiente tiene al menos min_keys + 1 claves
            elif len(node.children[idx + 1].keys) > self.min_keys:
                successor = self._get_successor(node.children[idx + 1])
                node.keys[idx] = successor
                self._delete(node.children[idx + 1], successor)
            # Caso 2c: Ambos hijos tienen exactamente min_keys claves
            else:
                self._merge_children(node, idx)
                self._delete(node.children[idx], key)
        # Caso 3: La clave no está en el nodo actual
        else:
            if node.leaf:
                return  # La clave no existe en el árbol
            
            # Asegurar que el hijo tiene suficientes claves
            if len(node.children[idx].keys) <= self.min_keys:
                self._fix_child(node, idx)
                # Después de arreglar, puede que hayamos cambiado el índice
                if idx > len(node.keys):
                    idx = len(node.keys)
            
            # Si fusionamos con el siguiente, procesamos idx, si fusionamos con el anterior, idx-1
            self._delete(node.children[idx], key)
    
    def _get_predecessor(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]
    
    def _get_successor(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]
    
    def _merge_children(self, parent, index):
        child = parent.children[index]
        sibling = parent.children[index + 1]
        
        # Mover la clave del padre al hijo
        child.keys.append(parent.keys.pop(index))
        
        # Mover las claves del hermano
        child.keys.extend(sibling.keys)
        
        # Mover los hijos del hermano si no es hoja
        if not sibling.leaf:
            child.children.extend(sibling.children)
        
        # Eliminar el hermano
        parent.children.pop(index + 1)
    
    def _fix_child(self, parent, index):
        # Intentar tomar prestado del hermano izquierdo
        if index > 0 and len(parent.children[index - 1].keys) > self.min_keys:
            self._borrow_from_left(parent, index)
        # Intentar tomar prestado del hermano derecho
        elif index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > self.min_keys:
            self._borrow_from_right(parent, index)
        # Fusionar con un hermano
        else:
            if index == len(parent.children) - 1:
                # Fusionar con el hermano izquierdo
                self._merge_children(parent, index - 1)
            else:
                # Fusionar con el hermano derecho
                self._merge_children(parent, index)
    
    def _borrow_from_left(self, parent, index):
        child = parent.children[index]
        left_sibling = parent.children[index - 1]
        
        # Mover la clave del padre al hijo
        child.keys.insert(0, parent.keys[index - 1])
        
        # Mover la clave máxima del hermano izquierdo al padre
        parent.keys[index - 1] = left_sibling.keys.pop()
        
        # Mover el hijo correspondiente si no es hoja
        if not left_sibling.leaf:
            child.children.insert(0, left_sibling.children.pop())
    
    def _borrow_from_right(self, parent, index):
        child = parent.children[index]
        right_sibling = parent.children[index + 1]
        
        # Mover la clave del padre al hijo
        child.keys.append(parent.keys[index])
        
        # Mover la clave mínima del hermano derecho al padre
        parent.keys[index] = right_sibling.keys.pop(0)
        
        # Mover el hijo correspondiente si no es hoja
        if not right_sibling.leaf:
            child.children.append(right_sibling.children.pop(0))
    
    def print_tree(self, node=None, level=0):
        if node is None:
            node = self.root
        
        print(f"Level {level}", end=": ")
        print(node.keys)
        
        if not node.leaf:
            for child in node.children:
                self.print_tree(child, level + 1)
    
    def change_order(self, new_order):
        if new_order < 3:
            raise ValueError("El orden del árbol B debe ser al menos 3")
        
        # Reconstruir el árbol con el nuevo orden
        if self.root is None or len(self.root.keys) == 0:
            self.order = new_order
            self.min_keys = (new_order - 1) // 2
            return
        
        # Recopilar todas las claves
        keys = []
        self._collect_keys(self.root, keys)
        
        # Recrear el árbol con el nuevo orden
        self.order = new_order
        self.min_keys = (new_order - 1) // 2
        self.root = BTreeNode(leaf=True)
        
        # Reinsertar todas las claves
        for key in keys:
            self.insert(key)
    
    def _collect_keys(self, node, keys):
        if node.leaf:
            keys.extend(node.keys)
        else:
            for i, key in enumerate(node.keys):
                self._collect_keys(node.children[i], keys)
                keys.append(key)
            self._collect_keys(node.children[-1], keys)


# Ejemplo de uso
if __name__ == "__main__":
    btree = BTree(order=4)  # Árbol B de orden 3 (2-3 árbol)
    
    print("Insertando claves...")
    for key in [0,1,2,3,4,5]:
        btree.insert(key)
        print(f"Insertado {key}:")
        btree.print_tree()
        print()
    
    print("Árbol completo:")
    btree.print_tree()

    btree.delete(3)

    print("\n")

    btree.print_tree()
    
