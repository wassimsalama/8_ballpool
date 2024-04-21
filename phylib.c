#include "phylib.h"

phylib_object *phylib_new_still_ball(unsigned char number, phylib_coord *pos) {
    // Allocate memory for a new phylib_object
    phylib_object *new_obj = (phylib_object *)malloc(sizeof(phylib_object));
    if (new_obj == NULL) {
        return NULL;  // Return NULL if memory allocation fails
    }


    // Set the type to PHYLIB_STILL_BALL and transfer the information
    new_obj->type = PHYLIB_STILL_BALL;
    new_obj->obj.still_ball.number = number;
    new_obj->obj.still_ball.pos.x= pos->x;
    new_obj->obj.still_ball.pos.y= pos->y;

    return new_obj;
}
phylib_object *phylib_new_rolling_ball( unsigned char number,phylib_coord *pos,phylib_coord *vel,phylib_coord *acc ){
    phylib_object *new_obj = (phylib_object *)malloc(sizeof(phylib_object));
    if(new_obj == NULL){ // Return NULL if memory allocation fails
        return NULL;
    }
    // Set the type to PHYLIB_ROLLING_BALL and transfer the information
    new_obj->type = PHYLIB_ROLLING_BALL;
    new_obj->obj.rolling_ball.pos = *pos;
    new_obj->obj.rolling_ball.vel = *vel;
    new_obj->obj.rolling_ball.acc = *acc;
    new_obj->obj.rolling_ball.number = number;

    return new_obj;
}
phylib_object *phylib_new_hole( phylib_coord *pos ){
     phylib_object *new_obj = (phylib_object *)malloc(sizeof(phylib_object));
    if(new_obj == NULL){ // Return NULL if memory allocation fails
        return NULL;
    }
     // Set the type to PHYLIB_HOLE and transfer the information
    new_obj->type = PHYLIB_HOLE;
    new_obj->obj.hole.pos = *pos;


    return new_obj;
}
phylib_object *phylib_new_hcushion( double y ){
      phylib_object *new_obj = (phylib_object *)malloc(sizeof(phylib_object));
    if(new_obj == NULL){ // Return NULL if memory allocation fails
        return NULL;
    } 
    // Set the type to PHYLIB_HCUSHION and transfer the information
    new_obj->type = PHYLIB_HCUSHION;
    new_obj->obj.hcushion.y = y;
    return new_obj;
}
phylib_object *phylib_new_vcushion( double x ){
      phylib_object *new_obj = (phylib_object *)malloc(sizeof(phylib_object));
    if(new_obj == NULL){ // Return NULL if memory allocation fails
        return NULL;
    }
    // Set the type to PHYLIB_VCUSHION and transfer the information
    new_obj->type = PHYLIB_VCUSHION;
    new_obj->obj.vcushion.x = x;
    return new_obj;
}
phylib_table *phylib_new_table(void) {
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));
    if (new_table == NULL) { // Return NULL if memory allocation fails
        return NULL;
    }

    // Define the positions for the holes
    phylib_coord corner_positions[6] = {
        {0.0, 0.0}, 
        {0.0,PHYLIB_TABLE_WIDTH}, 
        {0.0, PHYLIB_TABLE_LENGTH}, 
        {PHYLIB_TABLE_WIDTH,0.0}, 
        {PHYLIB_TABLE_WIDTH , PHYLIB_TABLE_WIDTH}, 
        {PHYLIB_TABLE_WIDTH , PHYLIB_TABLE_LENGTH} 
    };
    // set time to 0.0
    new_table->time = 0.0;

    // Add cushions
    new_table->object[0] = phylib_new_hcushion(0.0);
    new_table->object[1] = phylib_new_hcushion(PHYLIB_TABLE_LENGTH);
    new_table->object[2] = phylib_new_vcushion(0.0);
    new_table->object[3] = phylib_new_vcushion(PHYLIB_TABLE_WIDTH);

    // Add holes
    for (int i = 0; i < 6; i++) {
        new_table->object[4 + i] = phylib_new_hole(&corner_positions[i]);
    }

    // Initialize remaining objects as NULL
    for (int i = 10; i < PHYLIB_MAX_OBJECTS; i++) {
        new_table->object[i] = NULL;
    }

    return new_table;
}


void phylib_copy_object( phylib_object **dest, phylib_object **src ){
       if (!src || !*src) {
        *dest = NULL;
        return;
    }
     *dest = (phylib_object *)malloc(sizeof(phylib_object));
      memcpy(*dest, *src, sizeof(phylib_object)); // copying the data using memcpy
}
phylib_table *phylib_copy_table(phylib_table *table) {
    phylib_table *new_table = (phylib_table *)malloc(sizeof(phylib_table));
    if (!new_table) {
        return NULL;
    }

    new_table->time = table->time;

    // Initialize all objects in new_table to NULL
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        new_table->object[i] = NULL;
    }

    // Copy objects from the original table
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (table->object[i] != NULL) {
            phylib_copy_object(&new_table->object[i], &table->object[i]);
            if (new_table->object[i] == NULL) {
                // Clean up in case of failure
                for (int j = 0; j < i; j++) {
                    if (new_table->object[j] != NULL) {
                        free(new_table->object[j]);
                    }
                }
                free(new_table);
                return NULL;
            }
        }
    }

    return new_table;
}

void phylib_add_object( phylib_table *table, phylib_object *object ){
    // looping through the objects
    for(int i = 0 ; i < PHYLIB_MAX_OBJECTS ; i++){
        if(table->object[i] == NULL){
            table->object[i]= object; // adding the object
            break;
    }
}
}
void phylib_free_table( phylib_table *table ){
    for( int i = 0 ; i < PHYLIB_MAX_OBJECTS ; i++){
        if(table->object[i]!=NULL){ // checking if object isnt null
            free(table->object[i]) ;// free it if it is
        }
    }
    free(table);
}
phylib_coord phylib_sub( phylib_coord c1, phylib_coord c2 ){
    phylib_coord c;
    c.x=c1.x-c2.x;
    c.y=c1.y-c2.y;
    return c;
}
double phylib_length( phylib_coord c ){
     return sqrt(c.x * c.x + c.y * c.y); 
}
double phylib_dot_product( phylib_coord a, phylib_coord b ){
    double dot_product = (a.x * b.x) + (a.y*b.y);
    return dot_product;
}

double phylib_distance(phylib_object *obj1, phylib_object *obj2) {
    if (obj1 == NULL || obj2 == NULL || obj1->type != PHYLIB_ROLLING_BALL) {
        return -1.0;
    }

    phylib_coord diff;
    double distance;

    switch (obj2->type) {
        case PHYLIB_STILL_BALL: 
            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.still_ball.pos);//calculating distance between two balls
            distance = phylib_length(diff) - PHYLIB_BALL_DIAMETER; // subtracting diameter
            break;
        case PHYLIB_ROLLING_BALL:
            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.rolling_ball.pos);//calculating distance between two balls
            distance = phylib_length(diff) - PHYLIB_BALL_DIAMETER; // subtracting diameter
            break;

        case PHYLIB_HOLE:
            diff = phylib_sub(obj1->obj.rolling_ball.pos, obj2->obj.hole.pos);// calculating distance between ball center and hole
            distance = phylib_length(diff) - PHYLIB_HOLE_RADIUS;// subtracting hole radius 
            break;

        case PHYLIB_HCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.y - obj2->obj.hcushion.y) - PHYLIB_BALL_RADIUS; //distance between ball and cusion then subtract radius
            break;

        case PHYLIB_VCUSHION:
            distance = fabs(obj1->obj.rolling_ball.pos.x - obj2->obj.vcushion.x) - PHYLIB_BALL_RADIUS;
            break;

        default:
            return -1.0;
    }

    return distance;
}

void phylib_roll( phylib_object *new, phylib_object *old, double time ){
    if(new == NULL || old == NULL || old->type != PHYLIB_ROLLING_BALL || new->type != PHYLIB_ROLLING_BALL){
        return;
    }
     double oldPosX = old->obj.rolling_ball.pos.x;
     double oldPosY = old->obj.rolling_ball.pos.y;
     double oldVelX = old->obj.rolling_ball.vel.x;
     double oldVelY = old->obj.rolling_ball.vel.y;
     double oldAccelX = old->obj.rolling_ball.acc.x;
     double oldAccelY = old->obj.rolling_ball.acc.y;
     new->obj.rolling_ball.vel.x = oldVelX + oldAccelX * time;
     new->obj.rolling_ball.vel.y = oldVelY + oldAccelY * time;
     
     // Update positions
      new->obj.rolling_ball.pos.x = oldPosX+ oldVelX * time + 0.5 * oldAccelX * time * time;
      new->obj.rolling_ball.pos.y = oldPosY + oldVelY * time + 0.5 * oldAccelY * time * time;
       

      // Check for change in sign of velocity and adjust if necessary
        if ((new->obj.rolling_ball.vel.x * oldVelX) < 0) {
        new->obj.rolling_ball.vel.x = 0;
        new->obj.rolling_ball.acc.x = 0;
    }
    if ((new->obj.rolling_ball.vel.y * oldVelY) < 0) {
        new->obj.rolling_ball.vel.y = 0;
        new->obj.rolling_ball.acc.y = 0;
    }


}


unsigned char phylib_stopped( phylib_object *object ){

    double speed = phylib_length(object->obj.rolling_ball.vel); 
    if(speed < PHYLIB_VEL_EPSILON){ // checking if speed is less than PHYLIB_VEL_EPSILON
        phylib_object temp = *object;
        object->type = PHYLIB_STILL_BALL;
        object->obj.still_ball.number = temp.obj.rolling_ball.number;
        object->obj.still_ball.pos.x = temp.obj.rolling_ball.pos.x;
        object->obj.still_ball.pos.y = temp.obj.rolling_ball.pos.y;

        return 1;
    }

    return 0;
}

void phylib_bounce(phylib_object **a, phylib_object **b) {
    if (!a || !b || !*a || !*b) return; // Add safety checks

    phylib_coord r_ab, v_rel, n;
    double len_r_ab, v_rel_n;
    double speed_a, speed_b;
    phylib_coord temp;
    unsigned char temp_number;


    switch ((*b)->type) {
        case PHYLIB_HCUSHION:
            (*a)->obj.rolling_ball.vel.y *= -1; // negating if its HCUSHION
            (*a)->obj.rolling_ball.acc.y *= -1;
            break;

        case PHYLIB_VCUSHION:
            (*a)->obj.rolling_ball.vel.x *= -1; // negating if its VCUSHION
            (*a)->obj.rolling_ball.acc.x *= -1;
            break;

        case PHYLIB_HOLE:
            free(*a);
            *a = NULL;
            return;

        case PHYLIB_STILL_BALL:
            // Upgrade STILL_BALL to ROLLING_BALL and fall through to the next case
            temp.x = (*b)->obj.still_ball.pos.x;
            temp.y = (*b)->obj.still_ball.pos.y;
            temp_number = (*b)->obj.still_ball.number;

            (*b)->type = PHYLIB_ROLLING_BALL;
            (*b)->obj.rolling_ball.pos.x = temp.x;
            (*b)->obj.rolling_ball.pos.y = temp.y;
            (*b)->obj.rolling_ball.number = temp_number;
            (*b)->obj.rolling_ball.acc.x = 0.0;
            (*b)->obj.rolling_ball.acc.y = 0.0;
            (*b)->obj.rolling_ball.vel.x = 0.0;
            (*b)->obj.rolling_ball.vel.y = 0.0;

        case PHYLIB_ROLLING_BALL:
            // Calculate intermediate values for collision
            r_ab = phylib_sub((*a)->obj.rolling_ball.pos, (*b)->obj.rolling_ball.pos);
            v_rel = phylib_sub((*a)->obj.rolling_ball.vel, (*b)->obj.rolling_ball.vel);
            len_r_ab = phylib_length(r_ab);
            n.x = r_ab.x / len_r_ab;
            n.y = r_ab.y / len_r_ab;
            v_rel_n = phylib_dot_product(v_rel, n);

            // Update velocities of a and b
            (*a)->obj.rolling_ball.vel.x -= v_rel_n * n.x;
            (*a)->obj.rolling_ball.vel.y -= v_rel_n * n.y;
            (*b)->obj.rolling_ball.vel.x += v_rel_n * n.x;
            (*b)->obj.rolling_ball.vel.y += v_rel_n * n.y;

            // Adjust accelerations based on speed and PHYLIB_DRAG
            speed_a = phylib_length((*a)->obj.rolling_ball.vel);
            speed_b = phylib_length((*b)->obj.rolling_ball.vel);
            if (speed_a > PHYLIB_VEL_EPSILON) {
                (*a)->obj.rolling_ball.acc.x = -((*a)->obj.rolling_ball.vel.x / speed_a) * PHYLIB_DRAG;
                (*a)->obj.rolling_ball.acc.y = -((*a)->obj.rolling_ball.vel.y / speed_a) * PHYLIB_DRAG;
            }
            if (speed_b > PHYLIB_VEL_EPSILON) {
                (*b)->obj.rolling_ball.acc.x = -((*b)->obj.rolling_ball.vel.x / speed_b) * PHYLIB_DRAG;
                (*b)->obj.rolling_ball.acc.y = -((*b)->obj.rolling_ball.vel.y / speed_b) * PHYLIB_DRAG;
            }
            break;
    }
}

unsigned char phylib_rolling(phylib_table *t) {
    unsigned char count = 0;
    // looping over the objects and check if there are any rolling balls
    for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
        if (t->object[i]!=NULL && t->object[i]->type == PHYLIB_ROLLING_BALL) {
            count++;
        }
    }

    return count;
}

phylib_table *phylib_segment(phylib_table *table) {
    // Check for null table or no rolling balls
    if (table == NULL || phylib_rolling(table) == 0) {
        return NULL;
    }

    // Create a copy of the table
    phylib_table *copy = phylib_copy_table(table);
    if (copy == NULL) {
        return NULL; // Failed to create copy
    }

    double currentTime = table->time+PHYLIB_SIM_RATE; // Start from the current table time
    int stopOccurred = 0;

    // Process each simulation rate time step
    while (currentTime < PHYLIB_MAX_TIME && !stopOccurred ) {    
        for (int i = 0; i < PHYLIB_MAX_OBJECTS; i++) {
            if (copy->object[i] != NULL && copy->object[i]->type == PHYLIB_ROLLING_BALL) {
                // Apply rolling directly to the object
                phylib_roll(copy->object[i], copy->object[i], PHYLIB_SIM_RATE);
                
                // Check if ball has stopped
                if (phylib_stopped(copy->object[i])) {
                    copy->time = currentTime + PHYLIB_SIM_RATE;
                    return copy; // Return early as in the second version
                }

                // Check for collision with other objects
                for (int j = 0; j < PHYLIB_MAX_OBJECTS; j++) {
                    if (i != j && copy->object[j] != NULL && phylib_distance(copy->object[i], copy->object[j]) < 0.0) {
                        phylib_bounce(&(copy->object[i]), &(copy->object[j]));

                        stopOccurred = 1;
                        break; // Break inner loop on collision
                    }
                }
            }
        }

     if (!stopOccurred) {
            currentTime += PHYLIB_SIM_RATE; // Increment time only if no stop or collision occurred
        }
    }

    // Update time in the copied table if no early return
    copy->time = currentTime;
    return copy;
}

char *phylib_object_string( phylib_object *object ) {
    static char string[80]; if (object==NULL){
        snprintf( string, 80, "NULL;" ); return string;
    }   
    switch (object->type){
    case PHYLIB_STILL_BALL:
        snprintf( string, 80,
        "STILL_BALL (%d,%6.1lf,%6.1lf)",
        object->obj.still_ball.number, object->obj.still_ball.pos.x, object->obj.still_ball.pos.y );
        break;
    case PHYLIB_ROLLING_BALL: 
        snprintf( string, 80,
        "ROLLING_BALL (%d,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf,%6.1lf)", 
        object->obj.rolling_ball.number, object->obj.rolling_ball.pos.x, 
        object->obj.rolling_ball.pos.y, object->obj.rolling_ball.vel.x, 
        object->obj.rolling_ball.vel.y, 
        object->obj.rolling_ball.acc.x, 
        object->obj.rolling_ball.acc.y );
        break;
    case PHYLIB_HOLE: 
        snprintf( string, 80,
        "HOLE (%6.1lf,%6.1lf)", 
        object->obj.hole.pos.x, 
        object->obj.hole.pos.y );
        break;
    case PHYLIB_HCUSHION: 
        snprintf( string, 80,
        "HCUSHION (%6.1lf)", object->obj.hcushion.y );
        break;
    case PHYLIB_VCUSHION: 
        snprintf( string, 80,
        "VCUSHION (%6.1lf)", object->obj.vcushion.x );
        break; }
  return string;
}    


