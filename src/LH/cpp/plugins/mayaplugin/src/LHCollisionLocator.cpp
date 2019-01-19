#include "LHCollisionLocator.h"

MObject LHCollisionLocator::aSize;

MObject LHCollisionLocator::aPrimCapsuleType;
MObject LHCollisionLocator::aPrimCapsuleRadiusA;
MObject LHCollisionLocator::aPrimCapsuleRadiusB;
MObject LHCollisionLocator::aPrimCapsuleRadiusC;
MObject LHCollisionLocator::aPrimCapsuleRadiusD;
MObject LHCollisionLocator::aPrimLengthA;
MObject LHCollisionLocator::aPrimLengthB;

MTypeId LHCollisionLocator::id(10983797);
std::vector<std::vector<float>> newCircle = {{0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
                                             {-1.26431706078e-16f, 6.78573232311e-17f, -1.10819418755f},
                                             {-0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
                                             {-1.10819418755f, 1.96633546162e-32f, -3.21126950724e-16f},
                                             {-0.783611624891f, -4.79823734099e-17f, 0.783611624891f},
                                             {-3.33920536359e-16f, -6.78573232311e-17f, 1.10819418755f},
                                             {0.783611624891f, -4.79823734099e-17f, 0.783611624891f},
                                             {1.10819418755f, -3.6446300679e-32f, 5.95213259928e-16f},
                                             {0.783611624891f, 4.79823734099e-17f, -0.783611624891f},
                                             {-1.26431706078e-16f, 6.78573232311e-17f, -1.10819418755f},
                                             {-0.783611624891f, 4.79823734099e-17f, -0.783611624891f}};

std::vector<std::vector<float>> sphere = {{-5.36587337206e-16f, -6.12203396374e-17f, 0.999804019903f},
                                          {0.308956433194f, -5.8224002942e-17f, 0.950870128147f},
                                          {0.587670058082f, -4.95282951681e-17f, 0.808858443146f},
                                          {0.808858443146f, -3.59844127792e-17f, 0.587670058082f},
                                          {0.950870128147f, -1.89181253494e-17f, 0.308956433194f},
                                          {0.999804019903f, -3.57023946799e-32f, 5.83064353e-16f},
                                          {0.950870128147f, 1.89181253494e-17f, -0.308956433194f},
                                          {0.808858443146f, 3.59844127792e-17f, -0.587670058082f},
                                          {0.587670058082f, 4.95282951681e-17f, -0.808858443146f},
                                          {0.308956433194f, 5.8224002942e-17f, -0.950870128147f},
                                          {-6.16179902019e-17f, 6.12203396374e-17f, -0.999804019903f},
                                          {-0.308956433194f, 5.8224002942e-17f, -0.950870128147f},
                                          {-0.587670058082f, 4.95282951681e-17f, -0.808858443146f},
                                          {-0.808858443146f, 3.59844127792e-17f, -0.587670058082f},
                                          {-0.950870128147f, 1.89181253494e-17f, -0.308956433194f},
                                          {-0.999804019903f, 1.12083152919e-32f, -1.83045679778e-16f},
                                          {-0.950870128147f, -1.89181253494e-17f, 0.308956433194f},
                                          {-0.808858443146f, -3.59844127792e-17f, 0.587670058082f},
                                          {-0.587670058082f, -4.95282951681e-17f, 0.808858443146f},
                                          {-0.308956433194f, -5.8224002942e-17f, 0.950870128147f},
                                          {-5.36587337206e-16f, -6.12203396374e-17f, 0.999804019903f},
                                          {4.37515205623e-15f, 0.308956433194f, 0.950870128147f},
                                          {8.32203374572e-15f, 0.587670058082f, 0.808858443146f},
                                          {1.14542967892e-14f, 0.808858443146f, 0.587670058082f},
                                          {1.34653334561e-14f, 0.950870128147f, 0.308956433194f},
                                          {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
                                          {1.34653334561e-14f, 0.950870128147f, -0.308956433194f},
                                          {1.14542967892e-14f, 0.808858443146f, -0.587670058082f},
                                          {8.32203374572e-15f, 0.587670058082f, -0.808858443146f},
                                          {4.37515205623e-15f, 0.308956433194f, -0.950870128147f},
                                          {-6.16179902019e-17f, 6.12203396374e-17f, -0.999804019903f},
                                          {-4.37515205623e-15f, -0.308956433194f, -0.950870128147f},
                                          {-8.32203374572e-15f, -0.587670058082f, -0.808858443146f},
                                          {-1.14542967892e-14f, -0.808858443146f, -0.587670058082f},
                                          {-1.34653334561e-14f, -0.950870128147f, -0.308956433194f},
                                          {-5.36587337206e-16f, -0.999804019903f, 1.60780748964e-16f},
                                          {-1.34653334561e-14f, -0.950870128147f, 0.308956433194f},
                                          {-1.14542967892e-14f, -0.808858443146f, 0.587670058082f},
                                          {-8.32203374572e-15f, -0.587670058082f, 0.808858443146f},
                                          {-4.37515205623e-15f, -0.308956433194f, 0.950870128147f},
                                          {-5.36587337206e-16f, -6.12203396374e-17f, 0.999804019903f},
                                          {4.37515205623e-15f, 0.308956433194f, 0.950870128147f},
                                          {8.32203374572e-15f, 0.587670058082f, 0.808858443146f},
                                          {1.14542967892e-14f, 0.808858443146f, 0.587670058082f},
                                          {1.34653334561e-14f, 0.950870128147f, 0.308956433194f},
                                          {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
                                          {0.308956433194f, 0.950870128147f, -1.52911578997e-16f},
                                          {0.587670058082f, 0.808858443146f, -1.3007435828e-16f},
                                          {0.808858443146f, 0.587670058082f, -9.45045530938e-17f},
                                          {0.950870128147f, 0.308956433194f, -4.96839837983e-17f},
                                          {0.999804019903f, -3.57023946799e-32f, 5.83064353e-16f},
                                          {0.950870128147f, -0.308956433194f, 4.96839837983e-17f},
                                          {0.808858443146f, -0.587670058082f, 9.45045530938e-17f},
                                          {0.587670058082f, -0.808858443146f, 1.3007435828e-16f},
                                          {0.308956433194f, -0.950870128147f, 1.52911578997e-16f},
                                          {-5.36587337206e-16f, -0.999804019903f, 1.60780748964e-16f},
                                          {-0.308956433194f, -0.950870128147f, 1.52911578997e-16f},
                                          {-0.587670058082f, -0.808858443146f, 1.3007435828e-16f},
                                          {-0.808858443146f, -0.587670058082f, 9.45045530938e-17f},
                                          {-0.950870128147f, -0.308956433194f, 4.96839837983e-17f},
                                          {-0.999804019903f, 1.12083152919e-32f, -1.83045679778e-16f},
                                          {-0.950870128147f, 0.308956433194f, -4.96839837983e-17f},
                                          {-0.808858443146f, 0.587670058082f, -9.45045530938e-17f},
                                          {-0.587670058082f, 0.808858443146f, -1.3007435828e-16f},
                                          {-0.308956433194f, 0.950870128147f, -1.52911578997e-16f},
                                          {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f}};
std::vector<std::vector<int>> sphereIntArray = {{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                                                18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                                                34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49,
                                                50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65}};

// std::vector<std::vector<float>> capsuleStart = {{0.999804019903f, -3.57023946799e-32f, 5.83064353e-16f},
//                                                 {0.950870128147f, 1.89181253494e-17f, -0.308956433194f},
//                                                 {0.808858443146f, 3.59844127792e-17f, -0.587670058082f},
//                                                 {0.587670058082f, 4.95282951681e-17f, -0.808858443146f},
//                                                 {0.308956433194f, 5.8224002942e-17f, -0.950870128147f},
//                                                 {-6.16179902019e-17f, 6.12203396374e-17f, -0.999804019903f},
//                                                 {-0.308956433194f, 5.8224002942e-17f, -0.950870128147f},
//                                                 {-0.587670058082f, 4.95282951681e-17f, -0.808858443146f},
//                                                 {-0.808858443146f, 3.59844127792e-17f, -0.587670058082f},
//                                                 {-0.950870128147f, 1.89181253494e-17f, -0.308956433194f},
//                                                 {-0.999804019903f, 1.12083152919e-32f, -1.83045679778e-16f},
//                                                 {0.999804019928f, -3.69778549322e-32f, 6.10622663544e-16f},
//                                                 {0.0f, 0.0f, 0.0f},
//                                                 {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
//                                                 {1.34653334561e-14f, 0.950870128147f, -0.308956433194f},
//                                                 {1.14542967892e-14f, 0.808858443146f, -0.587670058082f},
//                                                 {8.32203374572e-15f, 0.587670058082f, -0.808858443146f},
//                                                 {4.37515205623e-15f, 0.308956433194f, -0.950870128147f},
//                                                 {-6.16179902019e-17f, 6.12203396374e-17f, -0.999804019903f},
//                                                 {-4.37515205623e-15f, -0.308956433194f, -0.950870128147f},
//                                                 {-8.32203374572e-15f, -0.587670058082f, -0.808858443146f},
//                                                 {-1.14542967892e-14f, -0.808858443146f, -0.587670058082f},
//                                                 {-1.34653334561e-14f, -0.950870128147f, -0.308956433194f},
//                                                 {-5.36587337206e-16f, -0.999804019903f, 1.60780748964e-16f},
//                                                 {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
//                                                 {0.308956433194f, 0.950870128147f, -1.52911578997e-16f},
//                                                 {0.587670058082f, 0.808858443146f, -1.3007435828e-16f},
//                                                 {0.808858443146f, 0.587670058082f, -9.45045530938e-17f},
//                                                 {0.950870128147f, 0.308956433194f, -4.96839837983e-17f},
//                                                 {0.999804019903f, -3.57023946799e-32f, 5.83064353e-16f},
//                                                 {0.950870128147f, -0.308956433194f, 4.96839837983e-17f},
//                                                 {0.808858443146f, -0.587670058082f, 9.45045530938e-17f},
//                                                 {0.587670058082f, -0.808858443146f, 1.3007435828e-16f},
//                                                 {0.308956433194f, -0.950870128147f, 1.52911578997e-16f},
//                                                 {-5.36587337206e-16f, -0.999804019903f, 1.60780748964e-16f},
//                                                 {-0.308956433194f, -0.950870128147f, 1.52911578997e-16f},
//                                                 {-0.587670058082f, -0.808858443146f, 1.3007435828e-16f},
//                                                 {-0.808858443146f, -0.587670058082f, 9.45045530938e-17f},
//                                                 {-0.950870128147f, -0.308956433194f, 4.96839837983e-17f},
//                                                 {-0.999804019903f, 1.12083152919e-32f, -1.83045679778e-16f},
//                                                 {-0.950870128147f, 0.308956433194f, -4.96839837983e-17f},
//                                                 {-0.808858443146f, 0.587670058082f, -9.45045530938e-17f},
//                                                 {-0.587670058082f, 0.808858443146f, -1.3007435828e-16f},
//                                                 {-0.308956433194f, 0.950870128147f, -1.52911578997e-16f},
//                                                 {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f}}

// std::vector<std::vector<float>> capsuleEnd = {{0.999804019903f, 1.23121221134e-16f, 1.0f},
//                                             {0.950870128147f, 1.42039346484e-16f, 1.30895643319f},
//                                             {0.808858443146f, 1.59105633913e-16f, 1.58767005808f},
//                                             {0.587670058082f, 1.72649516302e-16f, 1.80885844315f},
//                                             {0.308956433194f, 1.81345224076e-16f, 1.95087012815f},
//                                             {-6.16179902019e-17f, 1.84341560772e-16f, 1.9998040199f},
//                                             {-0.308956433194f, 1.81345224076e-16f, 1.95087012815f},
//                                             {-0.587670058082f, 1.72649516302e-16f, 1.80885844315f},
//                                             {-0.808858443146f, 1.59105633913e-16f, 1.58767005808f},
//                                             {-0.950870128147f, 1.42039346484e-16f, 1.30895643319f},
//                                             {-0.999804019903f, 1.23121221134e-16f, 1.0f},
//                                             {0.999804019928f, 1.23121221134e-16f, 1.0f},
//                                             {0.0f, 1.23121221134e-16f, 1.0f},
//                                             {-6.16179902019e-17f, -0.999804019903f, 1.0f},
//                                             {1.34653334561e-14f, -0.950870128147f, 1.30895643319f},
//                                             {1.14542967892e-14f, -0.808858443146f, 1.58767005808f},
//                                             {8.32203374572e-15f, -0.587670058082f, 1.80885844315f},
//                                             {4.37515205623e-15f, -0.308956433194f, 1.95087012815f},
//                                             {-6.16179902019e-17f, 1.84341560772e-16f, 1.9998040199f},
//                                             {-4.37515205623e-15f, 0.308956433194f, 1.95087012815f},
//                                             {-8.32203374572e-15f, 0.587670058082f, 1.80885844315f},
//                                             {-1.14542967892e-14f, 0.808858443146f, 1.58767005808f},
//                                             {-1.34653334561e-14f, 0.950870128147f, 1.30895643319f},
//                                             {-5.36587337206e-16f, 0.999804019903f, 1.0f},
//                                             {-6.16179902019e-17f, -0.999804019903f, 1.0f},
//                                             {0.308956433194f, -0.950870128147f, 1.0f},
//                                             {0.587670058082f, -0.808858443146f, 1.0f},
//                                             {0.808858443146f, -0.587670058082f, 1.0f},
//                                             {0.950870128147f, -0.308956433194f, 1.0f},
//                                             {0.999804019903f, 1.23121221134e-16f, 1.0f},
//                                             {0.950870128147f, 0.308956433194f, 1.0f},
//                                             {0.808858443146f, 0.587670058082f, 1.0f},
//                                             {0.587670058082f, 0.808858443146f, 1.0f},
//                                             {0.308956433194f, 0.950870128147f, 1.0f},
//                                             {-5.36587337206e-16f, 0.999804019903f, 1.0f},
//                                             {-0.308956433194f, 0.950870128147f, 1.0f},
//                                             {-0.587670058082f, 0.808858443146f, 1.0f},
//                                             {-0.808858443146f, 0.587670058082f, 1.0f},
//                                             {-0.950870128147f, 0.308956433194f, 1.0f},
//                                             {-0.999804019903f, 1.23121221134e-16f, 1.0f},
//                                             {-0.950870128147f, -0.308956433194f, 1.0f},
//                                             {-0.808858443146f, -0.587670058082f, 1.0f},
//                                             {-0.587670058082f, -0.808858443146f, 1.0f},
//                                             {-0.308956433194f, -0.950870128147f, 1.0f},
//                                             {-6.16179902019e-17f, -0.999804019903f, 1.0f}}
//First index is capsule start, second capsule end
std::vector<std::vector<float>> capsule = {{-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
                                           {-0.308956433194f, 0.950870128147f, -1.52911578997e-16f},
                                           {-0.587670058082f, 0.808858443146f, -1.3007435828e-16f},
                                           {-0.808858443146f, 0.587670058082f, -9.45045530938e-17f},
                                           {-0.950870128147f, 0.308956433194f, -4.96839837983e-17f},
                                           {-0.999804019903f, 1.12083152919e-32f, -1.83045679778e-16f},
                                           {-0.950870128147f, -0.308956433194f, 4.96839837983e-17f},
                                           {-0.808858443146f, -0.587670058082f, 9.45045530938e-17f},
                                           {-0.587670058082f, -0.808858443146f, 1.3007435828e-16f},
                                           {-0.308956433194f, -0.950870128147f, 1.52911578997e-16f},
                                           {-5.36587337206e-16f, -0.999804019903f, 1.60780748964e-16f},
                                           {0.308956433194f, -0.950870128147f, 1.52911578997e-16f},
                                           {0.587670058082f, -0.808858443146f, 1.3007435828e-16f},
                                           {0.808858443146f, -0.587670058082f, 9.45045530938e-17f},
                                           {0.950870128147f, -0.308956433194f, 4.96839837983e-17f},
                                           {0.999804019903f, -3.57023946799e-32f, 5.83064353e-16f},
                                           {0.950870128147f, 0.308956433194f, -4.96839837983e-17f},
                                           {0.808858443146f, 0.587670058082f, -9.45045530938e-17f},
                                           {0.587670058082f, 0.808858443146f, -1.3007435828e-16f},
                                           {0.308956433194f, 0.950870128147f, -1.52911578997e-16f},
                                           {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
                                           {-5.36587337206e-16f, -0.999804019903f, 1.60780748964e-16f},
                                           {-1.34653334561e-14f, -0.950870128147f, -0.308956433194f},
                                           {-1.14542967892e-14f, -0.808858443146f, -0.587670058082f},
                                           {-8.32203374572e-15f, -0.587670058082f, -0.808858443146f},
                                           {-4.37515205623e-15f, -0.308956433194f, -0.950870128147f},
                                           {-6.16179902019e-17f, 6.12203396374e-17f, -0.999804019903f},
                                           {4.37515205623e-15f, 0.308956433194f, -0.950870128147f},
                                           {8.32203374572e-15f, 0.587670058082f, -0.808858443146f},
                                           {1.14542967892e-14f, 0.808858443146f, -0.587670058082f},
                                           {1.34653334561e-14f, 0.950870128147f, -0.308956433194f},
                                           {-6.16179902019e-17f, 0.999804019903f, -1.60780748964e-16f},
                                           {0.0f, 0.0f, 0.0f},
                                           {0.999804019928f, -3.69778549322e-32f, 6.10622663544e-16f},
                                           {-0.999804019903f, 1.12083152919e-32f, -1.83045679778e-16f},
                                           {-0.950870128147f, 1.89181253494e-17f, -0.308956433194f},
                                           {-0.808858443146f, 3.59844127792e-17f, -0.587670058082f},
                                           {-0.587670058082f, 4.95282951681e-17f, -0.808858443146f},
                                           {-0.308956433194f, 5.8224002942e-17f, -0.950870128147f},
                                           {-6.16179902019e-17f, 6.12203396374e-17f, -0.999804019903f},
                                           {0.308956433194f, 5.8224002942e-17f, -0.950870128147f},
                                           {0.587670058082f, 4.95282951681e-17f, -0.808858443146f},
                                           {0.808858443146f, 3.59844127792e-17f, -0.587670058082f},
                                           {0.950870128147f, 1.89181253494e-17f, -0.308956433194f},
                                           {0.999804019928f, -3.69778549322e-32f, 5.82867087928e-16f},
                                           {0.999804019928f, 2.22044604925e-16f, 1.0f},
                                           {0.950870128147f, 1.42039346484e-16f, 1.30895643319f},
                                           {0.808858443146f, 1.59105633913e-16f, 1.58767005808f},
                                           {0.587670058082f, 1.72649516302e-16f, 1.80885844315f},
                                           {0.308956433194f, 1.81345224076e-16f, 1.95087012815f},
                                           {-6.16179902019e-17f, 1.84341560772e-16f, 1.9998040199f},
                                           {-0.308956433194f, 1.81345224076e-16f, 1.95087012815f},
                                           {-0.587670058082f, 1.72649516302e-16f, 1.80885844315f},
                                           {-0.808858443146f, 1.59105633913e-16f, 1.58767005808f},
                                           {-0.950870128147f, 1.42039346484e-16f, 1.30895643319f},
                                           {-0.999804019903f, 1.23121221134e-16f, 1.0f},
                                           {-0.999804019928f, 0.0f, -2.22044604925e-16f},
                                           {-0.999804019928f, 1.23121215202e-16f, 1.0f},
                                           {0.999804019928f, 1.23121221134e-16f, 1.0f},
                                           {0.0f, 1.23121221134e-16f, 1.0f},
                                           {-6.16179902019e-17f, -0.999804019903f, 1.0f},
                                           {1.34653334561e-14f, -0.950870128147f, 1.30895643319f},
                                           {1.14542967892e-14f, -0.808858443146f, 1.58767005808f},
                                           {8.32203374572e-15f, -0.587670058082f, 1.80885844315f},
                                           {4.37515205623e-15f, -0.308956433194f, 1.95087012815f},
                                           {-6.16179902019e-17f, 1.84341560772e-16f, 1.9998040199f},
                                           {-4.37515205623e-15f, 0.308956433194f, 1.95087012815f},
                                           {-8.32203374572e-15f, 0.587670058082f, 1.80885844315f},
                                           {-1.14542967892e-14f, 0.808858443146f, 1.58767005808f},
                                           {-1.34653334561e-14f, 0.950870128147f, 1.30895643319f},
                                           {-5.36587337206e-16f, 0.999804019903f, 1.0f},
                                           {0.0f, 0.999804019928f, 0.0f},
                                           {-4.99600361081e-16f, 0.999804019928f, 1.0f},
                                           {-5.55111512313e-17f, -0.999804019928f, 1.0f},
                                           {-5.55111512313e-16f, -0.999804019928f, 2.22044604925e-16f},
                                           {-6.16179902019e-17f, -0.999804019903f, 1.0f},
                                           {0.308956433194f, -0.950870128147f, 1.0f},
                                           {0.587670058082f, -0.808858443146f, 1.0f},
                                           {0.808858443146f, -0.587670058082f, 1.0f},
                                           {0.950870128147f, -0.308956433194f, 1.0f},
                                           {0.999804019903f, 1.23121221134e-16f, 1.0f},
                                           {0.950870128147f, 0.308956433194f, 1.0f},
                                           {0.808858443146f, 0.587670058082f, 1.0f},
                                           {0.587670058082f, 0.808858443146f, 1.0f},
                                           {0.308956433194f, 0.950870128147f, 1.0f},
                                           {-5.36587337206e-16f, 0.999804019903f, 1.0f},
                                           {-0.308956433194f, 0.950870128147f, 1.0f},
                                           {-0.587670058082f, 0.808858443146f, 1.0f},
                                           {-0.808858443146f, 0.587670058082f, 1.0f},
                                           {-0.950870128147f, 0.308956433194f, 1.0f},
                                           {-0.999804019903f, 1.23121221134e-16f, 1.0f},
                                           {-0.950870128147f, -0.308956433194f, 1.0f},
                                           {-0.808858443146f, -0.587670058082f, 1.0f},
                                           {-0.587670058082f, -0.808858443146f, 1.0f},
                                           {-0.308956433194f, -0.950870128147f, 1.0f},
                                           {-6.16179902019e-17f, -0.999804019903f, 1.0f}};
std::vector<std::vector<int>> capsuleIntArray{{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                                23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43,
                                                44, 56, 71, 74},
                                                {45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 57, 58, 59, 60, 61, 62, 63, 64,
                                                65, 66, 67, 68, 69, 70, 72, 73, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
                                                87, 88, 89, 90, 91, 92, 93, 94, 95}};


MString LHCollisionLocator::drawDbClassification("drawdb/geometry/LHCollisionLocator");

MString LHCollisionLocator::drawRegistrantId("LHCollisionLocatorPlugin");

LHCollisionLocator::LHCollisionLocator() {}

LHCollisionLocator::~LHCollisionLocator() {}

void* LHCollisionLocator::creator() {
  return new LHCollisionLocator();
}
// In case we need to implement in the future:
// bool LHCollisionLocator::isBounded() const
// {
//     return false;
// }
// MBoundingBox LHCollisionLocator::boundingBox() const
// {
//     static MBoundingBox circleBBox;
//     for (int i = 0; i < circleCount; i++)
//     {
//         MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
//         circleBBox.expand(shapePoint);
//     }
//     MBoundingBox bounds;
//     return bounds;
// }

LocatorCapsuleData getPlugValuesFromLocatorNode(const MDagPath &objPath)
{
    LocatorCapsuleData rData;
    // Retrieve value of the size attribute from the node
    MStatus status;
    MObject locatorNode = objPath.node(&status);

    // Put your objects into an array so you can loop through them by type
    MPlug plug(locatorNode, LHCollisionLocator::aSize);
    double val;
    plug.getValue(val);
    rData.size = val;

    MPlug radiusAPlug(locatorNode, LHCollisionLocator::aPrimCapsuleRadiusA);
    radiusAPlug.getValue(val);
    rData.dRadiusA = val;

    MPlug radiusBPlug(locatorNode, LHCollisionLocator::aPrimCapsuleRadiusB);
    radiusBPlug.getValue(val);
    rData.dRadiusB = val;

    MPlug radiusCPlug(locatorNode, LHCollisionLocator::aPrimCapsuleRadiusC);
    radiusCPlug.getValue(val);
    rData.dRadiusC = val;

    MPlug radiusDPlug(locatorNode, LHCollisionLocator::aPrimCapsuleRadiusD);
    radiusDPlug.getValue(val);
    rData.dRadiusD = val;


    MPlug lengthAPlug(locatorNode, LHCollisionLocator::aPrimLengthA);
    lengthAPlug.getValue(val);
    rData.dLengthA = val;

    MPlug lengthBPlug(locatorNode, LHCollisionLocator::aPrimLengthB);
    lengthBPlug.getValue(val);
    rData.dLengthB = val;


    MPlug eTypePlug(locatorNode, LHCollisionLocator::aPrimCapsuleType);
    short eVal;
    eTypePlug.getValue(eVal);
    rData.eType = eVal;


    //Get Locators World Matrix
    MPlug matrixPlug(locatorNode, LHCollisionLocator::worldMatrix);
    MFnMatrixData matrixData(matrixPlug.asMObject());
    MMatrix worldMatrix = matrixData.matrix();
    rData.mWorldMatrix = worldMatrix;


    // Start and end points
    MPoint pointStart(0.0, 0.0, 0.0);
    MPoint pointEnd(0.0, 0.0, 1.0);

    rData.pPointStart = pointStart * worldMatrix;
    rData.pPointEnd = pointEnd * worldMatrix;


    switch( rData.eType )
    {
        case 0 : // sphere
            rData.shape = sphere;
            rData.intArray = sphereIntArray;
            rData.doShapeA = true;
            rData.doShapeB = false;
            rData.doShapeC = false;
            break;
        case 1 : // elipsoidCapsule
            rData.shape = capsule;
            rData.intArray = capsuleIntArray;
            rData.doShapeA = true;
            rData.doShapeB = false;
            rData.doShapeC = false;
            break;
        case 2 : // elipsoid
            break;
        case 3 : // cylinder
            break;
        case 4 : // plane
            break;
        case 5 : // capsule
            break;
        case 6 : // cone
            break;
    }



    return rData;
}


MPoint drawType(MPoint inPoint, LocatorCapsuleData capsuleData)
{
    switch( capsuleData.eType )
    {
        case 0 : // sphere
            inPoint = inPoint + (inPoint - capsuleData.pPointStart) * (capsuleData.dRadiusA -1.0);
            break;
        case 1 : // elipsoidCapsule
            inPoint = inPoint + (inPoint - capsuleData.pPointStart) * (capsuleData.dRadiusA -1.0);
            break;
        case 2 : // elipsoid
            break;
        case 3 : // cylinder
            break;
        case 4 : // plane
            break;
        case 5 : // capsule
            break;
        case 6 : // cone
            break;
    }

    return inPoint;
}

//  void getShape(std::vector<std::vector<float>> &shape, LocatorCapsuleData capsuleData)
//  {
//      switch (capsuleData.eType)
//      {
//      case 0: // sphere
//          shape = sphere;
//          break;
//      case 1: // elipsoidCapsule
//          break;
//      case 2: // elipsoid
//          break;
//      case 3: // cylinder
//          break;
//      case 4: // plane
//          break;
//      case 5: // capsule
//          break;
//      case 6: // cone
//          break;
//      }


// }
void collectShapeData(LocatorCapsuleData plugData, MPointArray &shapePoints)
{
    if (shapePoints.length())
        shapePoints.clear();

    // std::vector<std::vector<float>> shape;

    // getShape(shape, plugData);

    for (int i = 0; i < plugData.shape.size(); i++)
    {
        MPoint shapePoint(plugData.shape[i][0], plugData.shape[i][1], plugData.shape[i][2]);
        shapePoint = drawType(shapePoint, plugData);
        shapePoints.append(shapePoint);
    }

}

void drawShape(MPointArray shapePoints, LocatorCapsuleData plugData)
{
    for (unsigned int i = 0; i < shapePoints.length(); ++i)
    {
        MPoint shapePoint(shapePoints[i][0], shapePoints[i][1], shapePoints[i][2]);
        shapePoint = drawType(shapePoint, plugData);
        glVertex3f(shapePoint.x, shapePoint.y, shapePoint.z);
    }
}

void LHCollisionLocator::draw(M3dView &view, const MDagPath &path,
                              M3dView::DisplayStyle style,
                              M3dView::DisplayStatus status)
{

    LocatorCapsuleData plugData = getPlugValuesFromLocatorNode(path);

    if (plugData.doShapeA)
        collectShapeData(plugData, plugData.shapePointsA);
    if (plugData.doShapeB)
        collectShapeData(plugData, plugData.shapePointsB);
    if (plugData.doShapeC)
        collectShapeData(plugData, plugData.shapePointsC);

    view.beginGL();

    if (plugData.doShapeA)
        glPushAttrib(GL_CURRENT_BIT);
        glBegin(GL_LINE_STRIP);
        drawShape(plugData.shapePointsA, plugData);
        glEnd();
        glPopAttrib();
    if (plugData.doShapeB)
        view.beginGL();
        glPushAttrib(GL_CURRENT_BIT);
        glBegin(GL_LINE_STRIP);
        drawShape(plugData.shapePointsB, plugData);
        glEnd();
        glPopAttrib();
    if (plugData.doShapeC)
        view.beginGL();
        glPushAttrib(GL_CURRENT_BIT);
        glBegin(GL_LINE_STRIP);
        drawShape(plugData.shapePointsC, plugData);
        glEnd();
        glPopAttrib();

    view.endGL();
}

LHCollisionLocatorOverride::LHCollisionLocatorOverride(const MObject& obj)
    : MPxDrawOverride(obj, NULL) {}

LHCollisionLocatorOverride::~LHCollisionLocatorOverride() {}

MHWRender::DrawAPI LHCollisionLocatorOverride::supportedDrawAPIs() const {
    return (MHWRender::kOpenGL | MHWRender::kDirectX11 | MHWRender::kOpenGLCoreProfile);
}

// bool LHCollisionLocatorOverride::isBounded(const MDagPath&, const MDagPath&) const {
//   return false;
// }

// MBoundingBox LHCollisionLocatorOverride::boundingBox(const MDagPath& objPath, const MDagPath& cameraPath) const {
//     static MBoundingBox circleBBox;
//     for (int i = 0; i < circleCount; i++)
//     {
//     MPoint shapePoint(circle[i][0], circle[i][1], circle[i][2]);
//     circleBBox.expand(shapePoint);
//     }
//     return circleBBox;
// }









MUserData* LHCollisionLocatorOverride::prepareForDraw(const MDagPath& objPath, const MDagPath& cameraPath,
                                                  const MHWRender::MFrameContext& frameContext, MUserData* oldData) {

    LocatorCapsuleData *data = dynamic_cast<LocatorCapsuleData *>(oldData);
    if (!data)
    {
        data = new LocatorCapsuleData();
    }

    LocatorCapsuleData plugData = getPlugValuesFromLocatorNode(objPath);
    data->doShapeA = plugData.doShapeA ;
    data->doShapeB = plugData.doShapeB ;
    data->doShapeB = plugData.doShapeB ;

    if (plugData.doShapeA)
        collectShapeData(plugData, data->shapePointsA);
    if (plugData.doShapeB)
        collectShapeData(plugData, data->shapePointsB);
    if (plugData.doShapeC)
        collectShapeData(plugData, data->shapePointsC);



    // if (data->shapePointsA.length())
    //     data->shapePointsA.clear();
    // std::vector<std::vector<float>> shape;
    // getShape(shape, plugData);

    // for (int i = 0; i < shape.size(); i++)
    // {
    //     MPoint shapePoint(shape[i][0], shape[i][1], shape[i][2]);
    //     shapePoint = drawType(shapePoint, plugData);
    //     data->shapePointsA.append(shapePoint);
    // }

    if (M3dView::displayStatus(objPath) == M3dView::kLead)
        data->mColor = M3dView::leadColor();

    if (M3dView::displayStatus(objPath) == M3dView::kActive)
        data->mColor = M3dView::hiliteColor();

    if (M3dView::displayStatus(objPath) == M3dView::kDormant)
        data->mColor = MColor(1.0, 0.0, 0.0, 1.0);

    if (M3dView::displayStatus(objPath) == M3dView::kActiveAffected)
        data->mColor = M3dView::activeAffectedColor();

    if (M3dView::displayStatus(objPath) == M3dView::kTemplate)
        data->mColor = M3dView::templateColor();
        
    if (M3dView::displayStatus(objPath) == M3dView::kActiveTemplate)
        data->mColor = M3dView::activeTemplateColor();

    if (frameContext.getDisplayStyle() == MFrameContext::kWireFrame)
        data->mColor = MHWRender::MGeometryUtilities::wireframeColor(objPath);
    return data;
}

void LHCollisionLocatorOverride::addUIDrawables(const MDagPath& objPath,
                                            MHWRender::MUIDrawManager& drawManager,
                                            const MHWRender::MFrameContext& frameContext,
                                            const MUserData* data) {
  const LocatorCapsuleData* drawData = dynamic_cast<const LocatorCapsuleData*>(data);
  if (!drawData) {
    return;
  }

    drawManager.beginDrawable();
    drawManager.setColor(drawData->mColor);
    drawManager.setLineWidth(1.0);
    drawManager.lineStrip(drawData->shapePointsA, false);
    drawManager.endDrawable();
}

MStatus LHCollisionLocator::initialize() {
  MStatus status;
  MFnNumericAttribute nAttr;
  MFnCompoundAttribute cAttr;
  MFnEnumAttribute eAttr;
  MFnUnitAttribute uAttr;

  aSize = nAttr.create("size", "sz", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aSize);

  aPrimCapsuleRadiusA = nAttr.create("capsuleRadiusA", "cradiusa", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusA);

  aPrimCapsuleRadiusB = nAttr.create("capsuleRadiusB", "cradiusb", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusB);

  aPrimCapsuleRadiusC = nAttr.create("capsuleRadiusC", "cradiusc", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusC);

  aPrimCapsuleRadiusD = nAttr.create("capsuleRadiusD", "cradiusd", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(1.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleRadiusD);

  aPrimLengthA = nAttr.create("pLengthA", "plena", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(0.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimLengthA);

  aPrimLengthB = nAttr.create("pLengthB", "plenb", MFnNumericData::kDouble);
  nAttr.setKeyable(true);
  nAttr.setWritable(true);
  nAttr.setStorable(true);
  nAttr.setDefault(0.0);
  nAttr.setReadable(true);
  nAttr.setChannelBox(true);
  addAttribute(aPrimLengthB);

  aPrimCapsuleType = eAttr.create("primType", "ptyp", 0);
  eAttr.addField( "sphere", 0 );
  eAttr.addField( "elipsoidCapsule", 1 );
  eAttr.addField( "elipsoid", 2 );
  eAttr.addField( "cylinder", 3 );
  eAttr.addField( "plane", 4 );
  eAttr.addField( "capsule", 5 );
  eAttr.addField( "cone", 6 );
  eAttr.setHidden( false );
  eAttr.setKeyable( true );
  eAttr.setWritable(true);
  eAttr.setStorable(true);
  eAttr.setChannelBox(true);
  addAttribute(aPrimCapsuleType);



  return MS::kSuccess;
}
