#include <iostream>
#include <fstream>
#include <string>
using namespace std;

const int M = 12;
const int K = 2;

class BloomFilter {
private:
    unsigned char bits[2];

public:

    BloomFilter() {
        clear();
    }

    int hash1(int x) {
        return x % M;
    }

    int hash2(int x) {
        return (x / M + 3) % M;
    }

    bool getBit(int i) {
        return (bits[i / 8] >> (i % 8)) & 1;
    }

    void setBit(int i) {
        bits[i / 8] = bits[i / 8] | (1 << (i % 8));
    }

    void insert(int x) {
        setBit(hash1(x));
        setBit(hash2(x));
    }

    bool contains(int x) {
        if (!getBit(hash1(x))) return false;
        if (!getBit(hash2(x))) return false;
        return true;
    }

    void clear() {
        bits[0] = 0;
        bits[1] = 0;
    }

    string estado() {
        string s = "[";

        for (int i = 0; i < M; i++) {
            if (i > 0) s += ",";
            s += to_string(getBit(i) ? 1 : 0);
        }

        s += "]";
        return s;
    }
};


int main() {

    BloomFilter bf;
    cout << "===== PRUEBA DEL BLOOM FILTER =====\n\n";
    cout << "1. Estado inicial:\n";
    cout << bf.estado() << "\n\n";

    int numeros[] = {10, 25, 50, 100};

    cout << "2. Prueba de funciones hash:\n";

    for (int x : numeros) {
        cout << "Numero: " << x << " | hash1 = " << bf.hash1(x) << " | hash2 = " << bf.hash2(x) << "\n";
    }
    cout << "\n";
    cout << "3. Insertando elementos...\n";
    bf.insert(10);
    cout << "Insertado: 10\n";
    cout << "Estado: " << bf.estado() << "\n\n";
    bf.insert(25);
    cout << "Insertado: 25\n";
    cout << "Estado: " << bf.estado() << "\n\n";
    bf.insert(50);
    cout << "Insertado: 50\n";
    cout << "Estado: " << bf.estado() << "\n\n";
    cout << "4. Probando contains():\n";
    int pruebas[] = {10, 25, 50, 100, 7, 30};
    for (int x : pruebas) {
        cout << "contains(" << x << ") = ";
        if (bf.contains(x))
            cout << "TRUE";
        else
            cout << "FALSE";
        cout << "\n";
    }
    cout << "\n";
    cout << "5. Bits del Bloom Filter:\n";
    for (int i = 0; i < M; i++) {
        cout << "bit[" << i << "] = " << bf.getBit(i) << "\n";
    }
    cout << "\n";
    cout << "6. Probando setBit():\n";
    bf.clear();
    cout << "Despues de clear(): " << bf.estado() << "\n";
    bf.setBit(3);
    bf.setBit(7);
    cout << "Despues de setBit(3) y setBit(7):\n";
    cout << bf.estado() << "\n\n";
    cout << "7. Probando clear():\n";
    bf.clear();
    cout << "Estado despues de clear():\n";
    cout << bf.estado() << "\n\n";
    cout << "8. Prueba final:\n";
    bf.insert(10);
    bf.insert(25);
    bf.insert(50);
    cout << "Elementos insertados: 10, 25, 50\n";
    cout << "Estado final: " << bf.estado() << "\n\n";
    cout << "10 -> " << (bf.contains(10) ? "SI" : "NO") << "\n";
    cout << "25 -> " << (bf.contains(25) ? "SI" : "NO") << "\n";
    cout << "50 -> " << (bf.contains(50) ? "SI" : "NO") << "\n";
    cout << "100 -> " << (bf.contains(100) ? "SI" : "NO") << "\n";
    return 0;
}