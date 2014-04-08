#ifndef _GCLX_H_
#define GCLX_H_ 1
/**
 * GCLX
 * ==========
 * This module is a main API header for the Geewa Client Library eXtended. 
 */

#include "common.h"
#include "client.h"

BEGIN_C_DECLS


typedef enum
{
    GCLX_ERROR = 0,
    GCLX_NET_DISCONECT,
    GCLX_NET_ONRECEIVE,
    GCLX_NET_ONCONNECTED
} gclx_event_type;


typedef enum
{
    GCLX_GAME_ERROR = 0,
} gclx_game_event_type;


typedef struct gclx_event_s
{
    gclx_event_type type;
    struct timeval t; // the timestamp
    void *value;
} gclx_event_t;

typedef struct gclx_game_event_s
{
    gclx_game_event_type type;
    struct timeval t; // the timestamp
    void *value;
} gclx_game_event_t;

typedef void (*gclx_event_listener)(gclx_event_t *, void *);
typedef void (*gclx_game_event_listener)(gclx_game_event_t *, void *);

typedef struct gclx_s
{
    gcl_client_t *channel;
    gcl_client_t *room;
} gclx_t;
    

/**
 * .. c:function:: gclx_t * gclx_client_new()
 * :return: pointer to the client structure.
 * Constructor of client structure.
 */
GCLX_EXTERN gclx_t * gclx_client_new();


/**
 * .. c:function:: gclx_t * gclx_client_init(gclx_t *gclx)
 * :param * gclx:  the client handle (pointer)
 * :return: gclx pointer or NULL
 * Initialize the client.
 */
GCLX_EXTERN gclx_t * gclx_client_init(gclx_t *gclx);

/**
 * .. c:function:: void gclx_client_destroy(gclx_t *gclx)
 * :param * gclx: the client handle (pointer)
 * Destructor for the client.
 */
GCLX_EXTERN void gclx_client_destroy(gclx_t *gclx);


/**
 * .. c:function:: gclx_t * gclx_connect(gclx_t *gclx, const char *URL, gcl_netproto_type proto);
 * :param * gclx: the client handle
 * :param string URL:  server name where to connect by default
 * :param gclx_netproto_type proto:  protocol to use, either HTTP, TCP or UDP(not supported by servers yet)
 * :return: gclx pointer or NULL on error
 * Connect the client to the server
 */
GCLX_EXTERN gclx_t * gclx_connect(gclx_t *gclx, const char *URL, gclx_netproto_type proto);

/**
 * .. c:function:: gclx_t * gclx_add_listener(gclx_t *gclx, gclx_event_type event, gclx_event_listener listener)
 * :param * gclx: the client handle
 * :param gclx_event_type event: event you are interested in
 * :param listener - callback function to be called on the event
 * :return: gclx pointer or NULL on error
 * Add a callback listener for non-game events like network and error states
 */
GCLX_EXTERN gclx_t * gclx_add_listener(gclx_t *gclx, gclx_event_type event, gclx_event_listener listener);

/**
 * .. c:function:: gclx_t * gclx_add_listener(gclx_t *gclx, gclx_game_event_type event, gclx_game_event_listener listener)
 * :param * gclx: the client handle
 * :param gclx_game_event_type event: event you are interested in
 * :param function listener: callback function to be called on the event
 * :return: gclx pointer or NULL on error
 * Add a callback listener for game specific events.
 */
GCLX_EXTERN gclx_t * gclx_add_game_listener(gclx_t *gclx, gclx_game_event_type event, gclx_game_event_listener listener);

END_C_DECLS

#endif /* GCLX_H_ */
