#pragma once

#define Error( msg ) \
    { \
    MString __txt = FormatError( msg, __FILE__, __LINE__ ); \
    MGlobal::displayError( __txt ); \
    cerr << endl << "Error: " << __txt; \
    } \

#define CheckBool( result ) \
    if( !(result) ) \
        { \
        Error( #result ); \
        }

#define CheckStatus( stat, msg ) \
    if( !stat ) \
        { \
        Error( msg ); \
        }

#define CheckObject( obj, msg ) \
    if(obj.isNull() ) \
        { \
        Error( msg ); \
        }

#define CheckStatusReturn( stat, msg ) \
    if( !stat ) \
        { \
        Error( msg ); \
        return stat; \
        }
;