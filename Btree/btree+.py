"""class Nodo:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []
        self.siguiente = None  # Solo para nodos hoja
        self.padre = None

class ArbolBPlus:
    def __init__(self, grado):
        self.raiz = Nodo(es_hoja=True)
        self.grado = grado
    
    def buscar(self, clave, nodo=None):
        if nodo is None:
            nodo = self.raiz
        
        if nodo.es_hoja:
            for i, k in enumerate(nodo.claves):
                if k == clave:
                    return (nodo, i)
            return None
        else:
            for i, k in enumerate(nodo.claves):
                if clave < k:
                    return self.buscar(clave, nodo.hijos[i])
            return self.buscar(clave, nodo.hijos[-1])
    
    def insertar(self, clave):
        hoja = self._encontrar_hoja(clave)
        self._insertar_en_hoja(hoja, clave)
        
        if len(hoja.claves) > self.grado - 1:
            self._dividir_nodo(hoja)
    
    def _encontrar_hoja(self, clave):
        actual = self.raiz
        while not actual.es_hoja:
            for i, k in enumerate(actual.claves):
                if clave < k:
                    actual = actual.hijos[i]
                    break
            else:
                actual = actual.hijos[-1]
        return actual
    
    def _insertar_en_hoja(self, nodo, clave):
        # Insertar la clave en orden
        for i, k in enumerate(nodo.claves):
            if clave < k:
                nodo.claves.insert(i, clave)
                return
        nodo.claves.append(clave)
    
    def _dividir_nodo(self, nodo):
        if len(nodo.claves) <= self.grado - 1:
            return
        
        medio = len(nodo.claves) // 2
        claves_izq = nodo.claves[:medio]
        claves_der = nodo.claves[medio:]
        
        nuevo_nodo = Nodo(es_hoja=nodo.es_hoja)
        nuevo_nodo.claves = claves_der
        nodo.claves = claves_izq
        
        if nodo.es_hoja:
            nuevo_nodo.siguiente = nodo.siguiente
            nodo.siguiente = nuevo_nodo
            nuevo_nodo.padre = nodo.padre
            clave_padre = claves_der[0]
        else:
            nuevo_nodo.hijos = nodo.hijos[medio:]
            nodo.hijos = nodo.hijos[:medio]
            for hijo in nuevo_nodo.hijos:
                hijo.padre = nuevo_nodo
            clave_padre = claves_der.pop(0)
        
        if nodo.padre is None:
            # Crear nueva raíz
            nueva_raiz = Nodo()
            nueva_raiz.claves = [clave_padre]
            nueva_raiz.hijos = [nodo, nuevo_nodo]
            nodo.padre = nueva_raiz
            nuevo_nodo.padre = nueva_raiz
            self.raiz = nueva_raiz
        else:
            padre = nodo.padre
            self._insertar_en_nodo_interno(padre, clave_padre, nuevo_nodo)
            if len(padre.claves) > self.grado - 1:
                self._dividir_nodo(padre)
    
    def _insertar_en_nodo_interno(self, nodo, clave, nuevo_hijo):
        # Insertar clave y nuevo_hijo en el nodo interno
        for i, k in enumerate(nodo.claves):
            if clave < k:
                nodo.claves.insert(i, clave)
                nodo.hijos.insert(i+1, nuevo_hijo)
                nuevo_hijo.padre = nodo
                return
        nodo.claves.append(clave)
        nodo.hijos.append(nuevo_hijo)
        nuevo_hijo.padre = nodo
    
    def eliminar(self, clave):
        resultado = self.buscar(clave)
        if resultado is None:
            return False  # La clave no existe
        
        hoja, idx = resultado
        self._eliminar_de_hoja(hoja, idx)
        
        if len(hoja.claves) < (self.grado // 2) and hoja != self.raiz:
            self._rebalancear(hoja)
        
        # Si la raíz queda vacía (excepto cuando es también hoja)
        if not self.raiz.es_hoja and len(self.raiz.claves) == 0:
            self.raiz = self.raiz.hijos[0]
            self.raiz.padre = None
        
        return True
    
    def _eliminar_de_hoja(self, nodo, idx):
        nodo.claves.pop(idx)
    
    def _rebalancear(self, nodo):
        padre = nodo.padre
        idx = padre.hijos.index(nodo)
        
        # Intentar redistribución con hermano izquierdo
        if idx > 0:
            hermano_izq = padre.hijos[idx-1]
            if len(hermano_izq.claves) > (self.grado // 2):
                self._redistribuir_izquierda(nodo, hermano_izq, padre, idx-1)
                return
        
        # Intentar redistribución con hermano derecho
        if idx < len(padre.hijos) - 1:
            hermano_der = padre.hijos[idx+1]
            if len(hermano_der.claves) > (self.grado // 2):
                self._redistribuir_derecha(nodo, hermano_der, padre, idx)
                return
        
        # Si no se puede redistribuir, fusionar
        if idx > 0:
            self._fusionar(hermano_izq, nodo, padre, idx-1)
        else:
            self._fusionar(nodo, hermano_der, padre, idx)
    
    def _redistribuir_izquierda(self, nodo, hermano, padre, idx_padre):
        if nodo.es_hoja:
            # Mover la última clave del hermano izquierdo al nodo
            clave_movida = hermano.claves.pop()
            nodo.claves.insert(0, clave_movida)
            padre.claves[idx_padre] = nodo.claves[0]
        else:
            # Mover la última clave y el último hijo
            clave_movida = hermano.claves.pop()
            hijo_movido = hermano.hijos.pop()
            nodo.claves.insert(0, padre.claves[idx_padre])
            nodo.hijos.insert(0, hijo_movido)
            hijo_movido.padre = nodo
            padre.claves[idx_padre] = clave_movida
    
    def _redistribuir_derecha(self, nodo, hermano, padre, idx_padre):
        if nodo.es_hoja:
            # Mover la primera clave del hermano derecho al nodo
            clave_movida = hermano.claves.pop(0)
            nodo.claves.append(clave_movida)
            padre.claves[idx_padre] = hermano.claves[0]
        else:
            # Mover la primera clave y el primer hijo
            clave_movida = hermano.claves.pop(0)
            hijo_movido = hermano.hijos.pop(0)
            nodo.claves.append(padre.claves[idx_padre])
            nodo.hijos.append(hijo_movido)
            hijo_movido.padre = nodo
            padre.claves[idx_padre] = clave_movida
    
    def _fusionar(self, nodo_izq, nodo_der, padre, idx_padre):
        if nodo_izq.es_hoja:
            # Fusionar hojas
            nodo_izq.claves += nodo_der.claves
            nodo_izq.siguiente = nodo_der.siguiente
            
            # Eliminar clave del padre
            padre.claves.pop(idx_padre)
            padre.hijos.pop(idx_padre + 1)
        else:
            # Fusionar nodos internos
            nodo_izq.claves.append(padre.claves.pop(idx_padre))
            nodo_izq.claves += nodo_der.claves
            nodo_izq.hijos += nodo_der.hijos
            for hijo in nodo_der.hijos:
                hijo.padre = nodo_izq
            padre.hijos.pop(idx_padre + 1)
        
        # Si el padre queda por debajo del mínimo y no es la raíz
        if len(padre.claves) < (self.grado // 2) and padre != self.raiz:
            self._rebalancear(padre)
    
    def imprimir(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        
        print(f"Nivel {nivel}: ", end="")
        print(nodo.claves, end="")
        if nodo.es_hoja:
            print(" (hoja)", end="")
        print()
        
        if not nodo.es_hoja:
            for hijo in nodo.hijos:
                self.imprimir(hijo, nivel+1)
    
    def imprimir_hojas(self):
        actual = self.raiz
        while not actual.es_hoja:
            actual = actual.hijos[0]
        
        while actual is not None:
            print(actual.claves, end=" -> ")
            actual = actual.siguiente
        print("None")

# Ejemplo de uso
if __name__ == "__main__":
    arbol = ArbolBPlus(grado=3)
    
    print("Insertando claves...")
    for clave in [0,1,2,3,4,5]:
        arbol.insertar(clave)
        print(f"Insertado {clave}")
        arbol.imprimir()
        print("Hojas:", end=" ")
        arbol.imprimir_hojas()
        print("-" * 50)
    
    print("\nEliminando claves...")
    for clave in [3,1]:
        arbol.eliminar(clave)
        print(f"Eliminado {clave}")
        arbol.imprimir()
        print("Hojas:", end=" ")
        arbol.imprimir_hojas()
        print("-" * 50)"""

class Nodo:
    def __init__(self, es_hoja=False):
        self.es_hoja = es_hoja
        self.claves = []
        self.hijos = []
        self.siguiente = None  # Solo para nodos hoja
        self.padre = None

class ArbolBPlus:
    def __init__(self, grado):
        self.raiz = Nodo(es_hoja=True)
        self.grado = grado
        self.min_claves = (grado // 2)
    
    def buscar(self, clave, nodo=None):
        if nodo is None:
            nodo = self.raiz
        
        if nodo.es_hoja:
            for i, k in enumerate(nodo.claves):
                if k == clave:
                    return (nodo, i)
            return None
        else:
            for i, k in enumerate(nodo.claves):
                if clave < k:
                    return self.buscar(clave, nodo.hijos[i])
            return self.buscar(clave, nodo.hijos[-1])
    
    def insertar(self, clave):
        hoja = self._encontrar_hoja(clave)
        self._insertar_en_hoja(hoja, clave)
        
        if len(hoja.claves) > self.grado - 1:
            self._dividir_nodo(hoja)
    
    def _encontrar_hoja(self, clave):
        actual = self.raiz
        while not actual.es_hoja:
            for i, k in enumerate(actual.claves):
                if clave < k:
                    actual = actual.hijos[i]
                    break
            else:
                actual = actual.hijos[-1]
        return actual
    
    def _insertar_en_hoja(self, nodo, clave):
        for i, k in enumerate(nodo.claves):
            if clave < k:
                nodo.claves.insert(i, clave)
                return
        nodo.claves.append(clave)
    
    def _dividir_nodo(self, nodo):
        if len(nodo.claves) <= self.grado - 1:
            return
        
        medio = len(nodo.claves) // 2
        claves_izq = nodo.claves[:medio]
        claves_der = nodo.claves[medio:]
        
        nuevo_nodo = Nodo(es_hoja=nodo.es_hoja)
        nuevo_nodo.claves = claves_der
        nodo.claves = claves_izq
        
        if nodo.es_hoja:
            nuevo_nodo.siguiente = nodo.siguiente
            nodo.siguiente = nuevo_nodo
            nuevo_nodo.padre = nodo.padre
            clave_padre = claves_der[0]
        else:
            nuevo_nodo.hijos = nodo.hijos[medio:]
            nodo.hijos = nodo.hijos[:medio]
            for hijo in nuevo_nodo.hijos:
                hijo.padre = nuevo_nodo
            clave_padre = claves_der.pop(0)
        
        if nodo.padre is None:
            nueva_raiz = Nodo()
            nueva_raiz.claves = [clave_padre]
            nueva_raiz.hijos = [nodo, nuevo_nodo]
            nodo.padre = nueva_raiz
            nuevo_nodo.padre = nueva_raiz
            self.raiz = nueva_raiz
        else:
            padre = nodo.padre
            self._insertar_en_nodo_interno(padre, clave_padre, nuevo_nodo)
            if len(padre.claves) > self.grado - 1:
                self._dividir_nodo(padre)
    
    def _insertar_en_nodo_interno(self, nodo, clave, nuevo_hijo):
        for i, k in enumerate(nodo.claves):
            if clave < k:
                nodo.claves.insert(i, clave)
                nodo.hijos.insert(i+1, nuevo_hijo)
                nuevo_hijo.padre = nodo
                return
        nodo.claves.append(clave)
        nodo.hijos.append(nuevo_hijo)
        nuevo_hijo.padre = nodo
    
    def eliminar(self, clave):
        resultado = self.buscar(clave)
        if resultado is None:
            return False
        
        nodo, idx = resultado
        self._eliminar_de_nodo(nodo, idx)
        
        if nodo != self.raiz and len(nodo.claves) < self.min_claves:
            self._rebalancear(nodo)
        
        # Si la raíz queda vacía (excepto cuando es también hoja)
        if not self.raiz.es_hoja and len(self.raiz.claves) == 0:
            self.raiz = self.raiz.hijos[0]
            self.raiz.padre = None
        
        return True
    
    def _eliminar_de_nodo(self, nodo, idx):
        if nodo.es_hoja:
            clave_eliminada = nodo.claves.pop(idx)
            
            # Actualizar clave en el padre si es necesario
            if idx == 0 and nodo.padre is not None and len(nodo.claves) > 0:
                self._actualizar_clave_padre(nodo, nodo.claves[0], clave_eliminada)
        else:
            # Para nodos internos, reemplazar con la clave más pequeña del subárbol derecho
            hijo_der = nodo.hijos[idx+1]
            while not hijo_der.es_hoja:
                hijo_der = hijo_der.hijos[0]
            nueva_clave = hijo_der.claves[0]
            nodo.claves[idx] = nueva_clave
            self._eliminar_de_nodo(hijo_der, 0)
            
            if len(hijo_der.claves) < self.min_claves:
                self._rebalancear(hijo_der)
    
    def _actualizar_clave_padre(self, nodo, nueva_clave, clave_vieja):
        padre = nodo.padre
        if padre is None:
            return
        
        for i, k in enumerate(padre.claves):
            if k == clave_vieja:
                padre.claves[i] = nueva_clave
                break
        
        # Si actualizamos la primera clave, propagar hacia arriba
        if i == 0 and padre.padre is not None:
            self._actualizar_clave_padre(padre, nueva_clave, clave_vieja)
    
    def _rebalancear(self, nodo):
        padre = nodo.padre
        idx = padre.hijos.index(nodo)
        
        # Intentar redistribución con hermano izquierdo
        hermano_izq = padre.hijos[idx-1] if idx > 0 else None
        hermano_der = padre.hijos[idx+1] if idx < len(padre.hijos) - 1 else None
        
        if hermano_izq and len(hermano_izq.claves) > self.min_claves:
            self._redistribuir_izquierda(nodo, hermano_izq, padre, idx-1)
            return
        
        if hermano_der and len(hermano_der.claves) > self.min_claves:
            self._redistribuir_derecha(nodo, hermano_der, padre, idx)
            return
        
        # Si no se puede redistribuir, fusionar
        if hermano_izq:
            self._fusionar(hermano_izq, nodo, padre, idx-1)
        elif hermano_der:
            self._fusionar(nodo, hermano_der, padre, idx)
    
    def _redistribuir_izquierda(self, nodo, hermano, padre, idx_padre):
        if nodo.es_hoja:
            # Mover la última clave del hermano izquierdo al nodo
            clave_movida = hermano.claves.pop()
            nodo.claves.insert(0, clave_movida)
            padre.claves[idx_padre] = nodo.claves[0]
        else:
            # Mover la última clave y el último hijo
            clave_movida = hermano.claves.pop()
            hijo_movido = hermano.hijos.pop()
            nodo.claves.insert(0, padre.claves[idx_padre])
            nodo.hijos.insert(0, hijo_movido)
            hijo_movido.padre = nodo
            padre.claves[idx_padre] = clave_movida
    
    def _redistribuir_derecha(self, nodo, hermano, padre, idx_padre):
        if nodo.es_hoja:
            # Mover la primera clave del hermano derecho al nodo
            clave_movida = hermano.claves.pop(0)
            nodo.claves.append(clave_movida)
            padre.claves[idx_padre] = hermano.claves[0]
        else:
            # Mover la primera clave y el primer hijo
            clave_movida = hermano.claves.pop(0)
            hijo_movido = hermano.hijos.pop(0)
            nodo.claves.append(padre.claves[idx_padre])
            nodo.hijos.append(hijo_movido)
            hijo_movido.padre = nodo
            padre.claves[idx_padre] = clave_movida
    
    def _fusionar(self, nodo_izq, nodo_der, padre, idx_padre):
        if nodo_izq.es_hoja:
            # Fusionar hojas
            nodo_izq.claves += nodo_der.claves
            nodo_izq.siguiente = nodo_der.siguiente
            
            # Eliminar clave del padre
            clave_eliminada = padre.claves.pop(idx_padre)
            padre.hijos.pop(idx_padre + 1)
            
            # Actualizar referencias si era la primera clave
            if idx_padre == 0 and padre.padre is not None:
                self._actualizar_clave_padre(padre, nodo_izq.claves[0], clave_eliminada)
        else:
            # Fusionar nodos internos
            clave_padre = padre.claves.pop(idx_padre)
            nodo_izq.claves.append(clave_padre)
            nodo_izq.claves += nodo_der.claves
            nodo_izq.hijos += nodo_der.hijos
            for hijo in nodo_der.hijos:
                hijo.padre = nodo_izq
            padre.hijos.pop(idx_padre + 1)
        
        # Si el padre queda por debajo del mínimo y no es la raíz
        if padre != self.raiz and len(padre.claves) < self.min_claves:
            self._rebalancear(padre)
    
    def imprimir(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        
        print(f"Nivel {nivel}: ", end="")
        print(nodo.claves, end="")
        if nodo.es_hoja:
            print(" (hoja)", end="")
        print()
        
        if not nodo.es_hoja:
            for hijo in nodo.hijos:
                self.imprimir(hijo, nivel+1)
    
    def imprimir_hojas(self):
        actual = self.raiz
        while not actual.es_hoja:
            actual = actual.hijos[0]
        
        while actual is not None:
            print(actual.claves, end=" -> ")
            actual = actual.siguiente
        print("None")

# Prueba exhaustiva
if __name__ == "__main__":
    arbol = ArbolBPlus(grado=3)
    datos = [10, 20, 5, 6, 12, 30, 7, 17]
    
    print("=== Insertando datos ===")
    for clave in datos:
        arbol.insertar(clave)
        print(f"Insertado: {clave}")
        arbol.imprimir()
        print("Hojas:", end=" ")
        arbol.imprimir_hojas()
        print("---")
    
    print("\n=== Verificando datos insertados ===")
    for clave in datos:
        res = arbol.buscar(clave)
        print(f"Clave {clave}: {'Encontrada' if res else 'No encontrada (ERROR)'}")
    
    print("\n=== Eliminando datos ===")
    eliminar = [6, 12, 17, 5, 20]
    for clave in eliminar:
        print(f"\nEliminando {clave}...")
        if arbol.eliminar(clave):
            print(f"Clave {clave} eliminada correctamente")
            arbol.imprimir()
            print("Hojas:", end=" ")
            arbol.imprimir_hojas()
            
            # Verificar que ya no existe
            res = arbol.buscar(clave)
            print(f"Verificación: {clave} {'aún existe (ERROR)' if res else 'eliminada correctamente'}")
        else:
            print(f"Clave {clave} no encontrada")
        print("---")
    
    print("\n=== Estado final del árbol ===")
    arbol.imprimir()
    print("Hojas:", end=" ")
    arbol.imprimir_hojas()
    
    print("\n=== Verificación final ===")
    for clave in datos:
        res = arbol.buscar(clave)
        if res:
            print(f"Clave {clave} aún presente en el árbol")
        else:
            print(f"Clave {clave} correctamente eliminada")