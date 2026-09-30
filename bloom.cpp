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

ofstream out("trace.json");
bool primero = true;

void escribir(string tag, string op, int x, string hashes, string antes, string despues, bool resultado) {
    if (!primero) out << ",";
    primero = false;
    out << "{\"tag\":\"" << tag << "\",\"op\":\"" << op << "\",\"x\":" << x
        << ",\"hashes\":" << hashes << ",\"before\":" << antes
        << ",\"after\":" << despues << ",\"result\":" << (resultado ? "true" : "false") << "}";
}

string hashesDe(BloomFilter& f, int x) {
    return "[" + to_string(f.hash1(x)) + "," + to_string(f.hash2(x)) + "]";
}

void hacerInsert(BloomFilter& f, string tag, int x) {
    string antes = f.estado();
    f.insert(x);
    escribir(tag, "insert", x, hashesDe(f, x), antes, f.estado(), false);
}

void hacerContains(BloomFilter& f, string tag, int x) {
    string antes = f.estado();
    bool r = f.contains(x);
    escribir(tag, "contains", x, hashesDe(f, x), antes, f.estado(), r);
}

int main() {
    BloomFilter f;
    out << "{\"m\":" << M << ",\"k\":" << K << ",\"events\":[";

    hacerContains(f, "empty", 7);
    hacerInsert(f, "insert5", 5);
    hacerInsert(f, "insert17", 17);
    hacerContains(f, "present", 5);
    hacerContains(f, "absent", 8);
    hacerContains(f, "false_positive", 15);
    hacerInsert(f, "duplicate", 17);

    string antes = f.estado();
    f.clear();
    escribir("clear", "clear", -1, "[]", antes, f.estado(), false);

    hacerContains(f, "after_clear", 5);

    out << "]}";
    out.close();
    return 0;
}