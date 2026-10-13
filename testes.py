"""Testes dos algoritmos do projeto; execute com python testes.py -v."""

import random
import unittest

from main import (
    arestas,
    circuito_euler,
    conexo,
    euleriano,
    gerar_grafo,
    grafo_de_arestas,
    graus,
    valida_circuito,
)


class TestesObrigatorios(unittest.TestCase):
    def test_ciclo_c4(self):
        grafo = grafo_de_arestas(4, [(1, 2), (2, 3), (3, 4), (4, 1)])
        self.assertEqual(graus(grafo), {1: 2, 2: 2, 3: 2, 4: 2})
        self.assertTrue(conexo(grafo))
        self.assertTrue(euleriano(grafo))
        self.assertTrue(valida_circuito(grafo, circuito_euler(grafo)))

    def test_caminho_p4(self):
        grafo = grafo_de_arestas(4, [(1, 2), (2, 3), (3, 4)])
        self.assertEqual(graus(grafo), {1: 1, 2: 2, 3: 2, 4: 1})
        self.assertTrue(conexo(grafo))
        self.assertFalse(euleriano(grafo))
        self.assertIsNone(circuito_euler(grafo))

    def test_dois_triangulos_desconexos(self):
        grafo = grafo_de_arestas(
            6, [(1, 2), (2, 3), (3, 1), (4, 5), (5, 6), (6, 4)]
        )
        self.assertTrue(all(g % 2 == 0 for g in graus(grafo).values()))
        self.assertFalse(conexo(grafo))
        self.assertFalse(euleriano(grafo))
        self.assertIsNone(circuito_euler(grafo))

    def test_grafo_vazio(self):
        grafo = grafo_de_arestas(4, [])
        self.assertEqual(graus(grafo), {1: 0, 2: 0, 3: 0, 4: 0})
        self.assertTrue(conexo(grafo))
        self.assertFalse(euleriano(grafo))
        self.assertIsNone(circuito_euler(grafo))
        self.assertFalse(valida_circuito(grafo, [1]))


class TestesExtras(unittest.TestCase):
    def test_ciclo_com_vertices_isolados(self):
        grafo = grafo_de_arestas(6, [(1, 2), (2, 3), (3, 4), (4, 1)])
        self.assertTrue(conexo(grafo))
        self.assertTrue(euleriano(grafo))
        self.assertTrue(valida_circuito(grafo, circuito_euler(grafo)))

    def test_borboleta_exige_unir_subciclos(self):
        grafo = grafo_de_arestas(
            5, [(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 1)]
        )
        circuito = circuito_euler(grafo)
        self.assertTrue(valida_circuito(grafo, circuito))
        self.assertEqual(circuito.count(1), 3)

    def test_k5(self):
        grafo = grafo_de_arestas(5, [(u, v) for u in range(1, 6)
                                      for v in range(u + 1, 6)])
        self.assertTrue(euleriano(grafo))
        self.assertTrue(valida_circuito(grafo, circuito_euler(grafo)))

    def test_construcao_nao_modifica_grafo(self):
        grafo = grafo_de_arestas(
            5, [(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 1)]
        )
        antes = {v: vizinhos.copy() for v, vizinhos in grafo.items()}
        circuito_euler(grafo)
        self.assertEqual(grafo, antes)

    def test_validador_rejeita_circuitos_invalidos(self):
        grafo = grafo_de_arestas(
            5, [(1, 2), (2, 3), (3, 1), (1, 4), (4, 5), (5, 1)]
        )
        self.assertFalse(valida_circuito(grafo, None))
        self.assertFalse(valida_circuito(grafo, [1, 2, 3, 1, 4, 5]))  # Aberto.
        self.assertFalse(valida_circuito(grafo, [1, 2, 3, 1]))  # Faltam arestas.
        self.assertFalse(valida_circuito(grafo, [1, 2, 3, 1, 2, 3, 1]))  # Repetidas.
        self.assertFalse(valida_circuito(grafo, [1, 2, 4, 5, 1, 3, 1]))  # (2, 4) não existe.

    def test_gerador_seed_simetria_limites(self):
        primeiro = gerar_grafo(10, 0.30, random.Random(482))
        segundo = gerar_grafo(10, 0.30, random.Random(482))
        self.assertEqual(primeiro, segundo)
        for u, vizinhos in primeiro.items():
            self.assertNotIn(u, vizinhos)
            for v in vizinhos:
                self.assertIn(u, primeiro[v])

        self.assertEqual(arestas(gerar_grafo(10, 0, random.Random(482))), [])
        completo = gerar_grafo(10, 1, random.Random(482))
        self.assertEqual(len(arestas(completo)), 45)
        self.assertFalse(euleriano(completo))

    def test_propriedade_em_grafos_aleatorios(self):
        rng = random.Random(391)
        for _ in range(500):
            grafo = gerar_grafo(10, 0.30, rng)
            circuito = circuito_euler(grafo)
            if euleriano(grafo):
                self.assertTrue(valida_circuito(grafo, circuito))
            else:
                self.assertIsNone(circuito)


if __name__ == "__main__":
    unittest.main()
