#include <iostream>
#include <stdlib.h>
// #include <cstdio>
// #include <cstdlib>
#include <vector>
#include <math.h>
#include <ctime>
using namespace std;

vector<double> getNormal(unsigned char* data, int* at);
void normalize(vector<double> &normal);

int main(int argc, char** argv) {
  int start_s = clock();

  FILE *fp;
  size_t size = 256 * 256 * 256;
  unsigned char *data = new unsigned char[size];
  unsigned char *normalx = new unsigned char[size];
  unsigned char *normaly = new unsigned char[size];
  unsigned char *normalz = new unsigned char[size];

  if (!(fp = fopen("../eucrib256.raw", "rb"))) {
      cout << "Error: opening .raw file failed" << endl;
      exit(EXIT_FAILURE);
  } else {
      cout << "OK: open .raw file successed" << endl;
  }

  if ( fread(data, sizeof(char), size, fp)!= size) {
      cout << "Error: read .raw file failed" << endl;
      exit(1);
  } else {
      cout << "OK: read .raw file successed" << endl;
  }

  fclose(fp);

  int at[3];

  for (size_t i = 0; i < size; i++) {
    at[0] = i % 256;
    at[1] = (i / 256) % 256;
    at[2] = i / (256 * 256);

    if (at[0] == 0 || at[1] == 0 || at[2] == 0 || at[0] == 255 || at[1] == 255 || at[2] == 255) {
      normalx[i] = (unsigned char)127;
      normaly[i] = (unsigned char)127;
      normalz[i] = (unsigned char)127;
      continue;
    }

    vector<double> normal = getNormal(data, at);

    normalize(normal);

    if (normal.at(0) > 255.0 || normal.at(1) > 255.0 || normal.at(2) > 255.0) {
      cout << normal.at(0) << ':' << normal.at(1) << ':' << normal.at(2) << "\n";
    }

    normalx[i] = (unsigned char)((int)round(normal.at(0)));
    normaly[i] = (unsigned char)((int)round(normal.at(1)));
    normalz[i] = (unsigned char)((int)round(normal.at(2)));

    if ((int)round(normal.at(0)) != (int)normalx[i]) {
      cout << (int)round(normal.at(0)) << " != " << (int)normalx[i] << endl;
    }

    cout << (i*100)/size << "\r";
  }

  FILE * pFilex;
  pFilex = fopen ("../normalx.raw", "wb");
  fwrite (normalx , sizeof(char), size, pFilex);
  fclose (pFilex);

  FILE * pFiley;
  pFiley = fopen ("../normaly.raw", "wb");
  fwrite (normaly , sizeof(char), size, pFiley);
  fclose (pFiley);

  FILE * pFilez;
  pFilez = fopen ("../normalz.raw", "wb");
  fwrite (normalz , sizeof(char), size, pFilez);
  fclose (pFilez);

  cout << "OK: Normal maps created" << endl;

  delete [] data;
  delete [] normalx;
  delete [] normaly;
  delete [] normalz;

  int stop_s = clock();
  cout << "time: " << (stop_s - start_s) / double(CLOCKS_PER_SEC) * 1000000 << " sec" << endl;
  return EXIT_SUCCESS;
}

vector<double> getNormal(unsigned char* data, int* at) {

    int texpos1[3];

    double w0 = (at[2] - 1) / 255.0;
    double w1 = at[2] / 255.0;
    double w2 = (at[2] + 1) / 255.0;

    double fx, fy, fz;

    double L[9];
    double H[9];

    texpos1[2] = at[2] - 1;
    for (int i = 2, k = 0; i > -1; --i) {
      for (int j = 0; j < 3; j++) {
        texpos1[0] = at[0] + (j - 1);
        texpos1[1] = at[1] + (i - 1);
        L[k] = (double)data[256 * 256 * texpos1[2] + 256 * texpos1[1] + texpos1[0]] / 255.0;
        H[k++] = (double)data[256 * 256 * (at[2] + 1) + 256 * texpos1[1] + texpos1[0]] / 255.0;
      }
    }

    // we need to get interpolation of 2 x points
    // x direction
    // -1 -3 -1   0  0  0   1  3  1
    // -3 -6 -3   0  0  0   3  6  3
    // -1 -3 -1   0  0  0   1  3  1
    // y direction
    //  1  3  1   3  6  3   1  3  1
    //  0  0  0   0  0  0   0  0  0
    // -1 -3 -1  -3 -6 -3  -1 -3 -1
    // z direction
    // -1  0  1   -3  0  3   -1  0  1
    // -3  0  3   -6  0  6   -3  0  3
    // -1  0  1   -3  0  3   -1  0  1

    fx =  ((w0 * (H[0] - L[0])) + L[0]) * -1.0;
    fx += ((w1 * (H[0] - L[0])) + L[0]) * -3.0;
    fx += ((w2 * (H[0] - L[0])) + L[0]) * -1.0;

    fx += ((w0 * (H[3] - L[3])) + L[3]) * -3.0;
    fx += ((w1 * (H[3] - L[3])) + L[3]) * -6.0;
    fx += ((w2 * (H[3] - L[3])) + L[3]) * -3.0;

    fx += ((w0 * (H[6] - L[6])) + L[6]) * -1.0;
    fx += ((w1 * (H[6] - L[6])) + L[6]) * -3.0;
    fx += ((w2 * (H[6] - L[6])) + L[6]) * -1.0;

    fx += ((w0 * (H[1] - L[1])) + L[1]) * 0.0;
    fx += ((w1 * (H[1] - L[1])) + L[1]) * 0.0;
    fx += ((w2 * (H[1] - L[1])) + L[1]) * 0.0;

    fx += ((w0 * (H[4] - L[4])) + L[4]) * 0.0;
    fx += ((w1 * (H[4] - L[4])) + L[4]) * 0.0;
    fx += ((w2 * (H[4] - L[4])) + L[4]) * 0.0;

    fx += ((w0 * (H[7] - L[7])) + L[7]) * 0.0;
    fx += ((w1 * (H[7] - L[7])) + L[7]) * 0.0;
    fx += ((w2 * (H[7] - L[7])) + L[7]) * 0.0;

    fx += ((w0 * (H[2] - L[2])) + L[2]) * 1.0;
    fx += ((w1 * (H[2] - L[2])) + L[2]) * 3.0;
    fx += ((w2 * (H[2] - L[2])) + L[2]) * 1.0;

    fx += ((w0 * (H[5] - L[5])) + L[5]) * 3.0;
    fx += ((w1 * (H[5] - L[5])) + L[5]) * 6.0;
    fx += ((w2 * (H[5] - L[5])) + L[5]) * 3.0;

    fx += ((w0 * (H[8] - L[8])) + L[8]) * 1.0;
    fx += ((w1 * (H[8] - L[8])) + L[8]) * 3.0;
    fx += ((w2 * (H[8] - L[8])) + L[8]) * 1.0;

    fy =  ((w0 * (H[0] - L[0])) + L[0]) * 1.0;
    fy += ((w1 * (H[0] - L[0])) + L[0]) * 3.0;
    fy += ((w2 * (H[0] - L[0])) + L[0]) * 1.0;

    fy += ((w0 * (H[3] - L[3])) + L[3]) * 0.0;
    fy += ((w1 * (H[3] - L[3])) + L[3]) * 0.0;
    fy += ((w2 * (H[3] - L[3])) + L[3]) * 0.0;

    fy += ((w0 * (H[6] - L[6])) + L[6]) * -1.0;
    fy += ((w1 * (H[6] - L[6])) + L[6]) * -3.0;
    fy += ((w2 * (H[6] - L[6])) + L[6]) * -1.0;

    fy += ((w0 * (H[1] - L[1])) + L[1]) * 3.0;
    fy += ((w1 * (H[1] - L[1])) + L[1]) * 6.0;
    fy += ((w2 * (H[1] - L[1])) + L[1]) * 3.0;

    fy += ((w0 * (H[4] - L[4])) + L[4]) * 0.0;
    fy += ((w1 * (H[4] - L[4])) + L[4]) * 0.0;
    fy += ((w2 * (H[4] - L[4])) + L[4]) * 0.0;

    fy += ((w0 * (H[7] - L[7])) + L[7]) * -3.0;
    fy += ((w1 * (H[7] - L[7])) + L[7]) * -6.0;
    fy += ((w2 * (H[7] - L[7])) + L[7]) * -3.0;

    fy += ((w0 * (H[2] - L[2])) + L[2]) * 1.0;
    fy += ((w1 * (H[2] - L[2])) + L[2]) * 3.0;
    fy += ((w2 * (H[2] - L[2])) + L[2]) * 1.0;

    fy += ((w0 * (H[5] - L[5])) + L[5]) * 0.0;
    fy += ((w1 * (H[5] - L[5])) + L[5]) * 0.0;
    fy += ((w2 * (H[5] - L[5])) + L[5]) * 0.0;

    fy += ((w0 * (H[8] - L[8])) + L[8]) * -1.0;
    fy += ((w1 * (H[8] - L[8])) + L[8]) * -3.0;
    fy += ((w2 * (H[8] - L[8])) + L[8]) * -1.0;


    fz =  ((w0 * (H[0] - L[0])) + L[0]) * -1.0;
    fz += ((w1 * (H[0] - L[0])) + L[0]) * 0.0;
    fz += ((w2 * (H[0] - L[0])) + L[0]) * 1.0;

    fz += ((w0 * (H[3] - L[3])) + L[3]) * -3.0;
    fz += ((w1 * (H[3] - L[3])) + L[3]) * 0.0;
    fz += ((w2 * (H[3] - L[3])) + L[3]) * 3.0;

    fz += ((w0 * (H[6] - L[6])) + L[6]) * -1.0;
    fz += ((w1 * (H[6] - L[6])) + L[6]) * 0.0;
    fz += ((w2 * (H[6] - L[6])) + L[6]) * 1.0;

    fz += ((w0 * (H[1] - L[1])) + L[1]) * -3.0;
    fz += ((w1 * (H[1] - L[1])) + L[1]) * 0.0;
    fz += ((w2 * (H[1] - L[1])) + L[1]) * 3.0;

    fz += ((w0 * (H[4] - L[4])) + L[4]) * -6.0;
    fz += ((w1 * (H[4] - L[4])) + L[4]) * 0.0;
    fz += ((w2 * (H[4] - L[4])) + L[4]) * 6.0;

    fz += ((w0 * (H[7] - L[7])) + L[7]) * -3.0;
    fz += ((w1 * (H[7] - L[7])) + L[7]) * 0.0;
    fz += ((w2 * (H[7] - L[7])) + L[7]) * 3.0;

    fz += ((w0 * (H[2] - L[2])) + L[2]) * -1.0;
    fz += ((w1 * (H[2] - L[2])) + L[2]) * 0.0;
    fz += ((w2 * (H[2] - L[2])) + L[2]) * 1.0;

    fz += ((w0 * (H[5] - L[5])) + L[5]) * -3.0;
    fz += ((w1 * (H[5] - L[5])) + L[5]) * 0.0;
    fz += ((w2 * (H[5] - L[5])) + L[5]) * 3.0;

    fz += ((w0 * (H[8] - L[8])) + L[8]) * -1.0;
    fz += ((w1 * (H[8] - L[8])) + L[8]) * 0.0;
    fz += ((w2 * (H[8] - L[8])) + L[8]) * 1.0;

    vector<double> normal;
    normal.push_back(fx/27.0);
    normal.push_back(fy/27.0);
    normal.push_back(fz/27.0);
    return normal;
}

void normalize(vector<double> &normal) {
  double length = sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2]);
  if (length == 0.0) {
    return;
  }
  double x = normal[0] / length;
  double y = normal[1] / length;
  double z = normal[2] / length;
  normal[0] = (x + 1.0) * 127.0;
  normal[1] = (y + 1.0) * 127.0;
  normal[2] = (z + 1.0) * 127.0;
}
