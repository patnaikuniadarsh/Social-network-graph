#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_SIZE 100
#define NAME_LENGTH 50
#define DATA_FILE "network_data.txt"

char names[MAX_SIZE][NAME_LENGTH];
int adjMatrix[MAX_SIZE][MAX_SIZE] = {0};
int num_people = 0;

// ---------------- Function Prototypes ----------------
int get_id(const char *name);
void initialize_network();
void save_network_to_file(const char *filename);
void load_network_from_file(const char *filename);
void add_user_or_friendship_interactive();
void add_user_or_friendship_noninteractive(const char *name1, const char *name2);
void show_network();
void suggest_mutual_friends();
void find_shortest_connection();
void display_menu();

// ---------------- Helper Function ----------------
int get_id(const char *name) {
    for (int i = 0; i < num_people; i++)
        if (strcmp(names[i], name) == 0)
            return i;
    return -1;
}

// ---------------- Initialization ----------------
void initialize_network() {
    // default set
    strcpy(names[0], "Joshnavi");
    strcpy(names[1], "Adarsh");
    strcpy(names[2], "Geetesh");
    strcpy(names[3], "Chandu");
    strcpy(names[4], "Kavya");

    num_people = 5;

    // clear matrix
    for (int i = 0; i < MAX_SIZE; i++)
        for (int j = 0; j < MAX_SIZE; j++)
            adjMatrix[i][j] = 0;

    int connections[][2] = {
        {0, 1}, {0, 2}, {1, 2}, {1, 3}, {2, 4}, {3, 4}
    };

    for (int i = 0; i < 6; i++) {
        int a = connections[i][0];
        int b = connections[i][1];
        adjMatrix[a][b] = 1;
        adjMatrix[b][a] = 1;
    }
}

// ---------------- File Operations ----------------
void save_network_to_file(const char *filename) {
    FILE *fp = fopen(filename, "w");
    if (!fp) {
        printf("Error: Cannot open file for writing.\n");
        return;
    }

    fprintf(fp, "%d\n", num_people);
    for (int i = 0; i < num_people; i++)
        fprintf(fp, "%s\n", names[i]);

    for (int i = 0; i < num_people; i++) {
        for (int j = 0; j < num_people; j++)
            fprintf(fp, "%d ", adjMatrix[i][j]);
        fprintf(fp, "\n");
    }

    fclose(fp);
}

void load_network_from_file(const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        // no file: initialize default
        initialize_network();
        save_network_to_file(filename);
        return;
    }

    if (fscanf(fp, "%d\n", &num_people) != 1) {
        // corrupted file: re-init
        fclose(fp);
        initialize_network();
        save_network_to_file(filename);
        return;
    }

    for (int i = 0; i < num_people; i++) {
        if (fscanf(fp, "%49s\n", names[i]) != 1) {
            // fallback
            strcpy(names[i], "Unknown");
        }
    }

    for (int i = 0; i < num_people; i++)
        for (int j = 0; j < num_people; j++)
            if (fscanf(fp, "%d", &adjMatrix[i][j]) != 1)
                adjMatrix[i][j] = 0;

    fclose(fp);
}

// ---------------- Feature: Add (interactive) ----------------
void add_user_or_friendship_interactive() {
    char new_name[NAME_LENGTH], conn1_name[NAME_LENGTH];

    printf("\n--- Add User/Friendship ---\n");
    printf("Enter name: ");
    if (scanf("%49s", new_name) != 1) { while (getchar() != '\n'); return; }

    int id1 = get_id(new_name);
    if (id1 == -1) {
        if (num_people >= MAX_SIZE) {
            printf("Error: Network full.\n");
            return;
        }
        strcpy(names[num_people], new_name);
        id1 = num_people++;
        printf("New user '%s' added.\n", new_name);
    }

    printf("Connect with: ");
    if (scanf("%49s", conn1_name) != 1) { while (getchar() != '\n'); return; }

    int id2 = get_id(conn1_name);
    if (id2 == -1) {
        printf("User '%s' not found.\n", conn1_name);
        return;
    }

    if (id1 == id2) {
        printf("Cannot connect user to themselves.\n");
        return;
    }
    if (adjMatrix[id1][id2] == 1) {
        printf("They are already connected.\n");
        return;
    }

    adjMatrix[id1][id2] = adjMatrix[id2][id1] = 1;
    printf("Connection between %s and %s added successfully!\n", new_name, conn1_name);
    save_network_to_file(DATA_FILE);
}

// ---------------- Feature: Add (noninteractive) ----------------
void add_user_or_friendship_noninteractive(const char *name1, const char *name2) {
    if (name1 == NULL || name2 == NULL) return;
    load_network_from_file(DATA_FILE); // ensure we have fresh data

    int id1 = get_id(name1);
    if (id1 == -1) {
        if (num_people >= MAX_SIZE) return;
        strcpy(names[num_people], name1);
        id1 = num_people++;
    }
    int id2 = get_id(name2);
    if (id2 == -1) {
        // cannot create connection if friend missing — we'll create friend
        if (num_people >= MAX_SIZE) return;
        strcpy(names[num_people], name2);
        id2 = num_people++;
    }
    if (id1 == id2) return;
    adjMatrix[id1][id2] = adjMatrix[id2][id1] = 1;
    save_network_to_file(DATA_FILE);
}

// ---------------- Feature 2: Show Network ----------------
void show_network() {
    printf("\n--- Current Network ---\n");
    for (int i = 0; i < num_people; i++) {
        printf("%-10s : ", names[i]);
        int count = 0;
        for (int j = 0; j < num_people; j++) {
            if (adjMatrix[i][j] == 1) {
                if (count > 0) printf(", ");
                printf("%s", names[j]);
                count++;
            }
        }
        if (count == 0) printf("None");
        printf("\n");
    }
}

// ---------------- Feature 3: Mutual Friends ----------------
void suggest_mutual_friends() {
    char name1[NAME_LENGTH], name2[NAME_LENGTH];
    printf("\n--- Mutual Friends ---\n");
    printf("User 1: ");
    if (scanf("%49s", name1) != 1) { while (getchar() != '\n'); return; }
    printf("User 2: ");
    if (scanf("%49s", name2) != 1) { while (getchar() != '\n'); return; }

    int id1 = get_id(name1);
    int id2 = get_id(name2);

    if (id1 == -1 || id2 == -1) {
        printf("Invalid input.\n");
        return;
    }

    printf("Mutual friends between %s and %s:\n", name1, name2);
    int found = 0;
    for (int i = 0; i < num_people; i++) {
        if (adjMatrix[id1][i] && adjMatrix[id2][i]) {
            printf("  -> %s\n", names[i]);
            found = 1;
        }
    }
    if (!found) printf("  -> None\n");
}

// ---------------- Feature 4: Shortest Connection (BFS) ----------------
void find_shortest_connection() {
    char s_name[NAME_LENGTH], e_name[NAME_LENGTH];
    printf("\n--- Shortest Connection ---\n");
    printf("Start Name: ");
    if (scanf("%49s", s_name) != 1) { while (getchar() != '\n'); return; }
    printf("End Name: ");
    if (scanf("%49s", e_name) != 1) { while (getchar() != '\n'); return; }

    int start = get_id(s_name);
    int end = get_id(e_name);
    if (start == -1 || end == -1) {
        printf("Invalid names.\n");
        return;
    }

    int queue[MAX_SIZE], parent[MAX_SIZE];
    bool visited[MAX_SIZE] = {false};
    int front = 0, rear = 0;

    for (int i = 0; i < num_people; i++) parent[i] = -1;
    queue[rear++] = start;
    visited[start] = true;

    while (front < rear) {
        int u = queue[front++];
        if (u == end) break;
        for (int v = 0; v < num_people; v++) {
            if (adjMatrix[u][v] && !visited[v]) {
                visited[v] = true;
                parent[v] = u;
                queue[rear++] = v;
            }
        }
    }

    if (!visited[end]) {
        printf("No connection found.\n");
        return;
    }

    int path[MAX_SIZE], len = 0;
    for (int v = end; v != -1; v = parent[v])
        path[len++] = v;

    printf("Path: ");
    for (int i = len - 1; i >= 0; i--) {
        printf("%s", names[path[i]]);
        if (i > 0) printf(" -> ");
    }
    printf("\nCost: %d\n", len - 1);
}

// ---------------- Menu ----------------
void display_menu() {
    printf("\n==================================\n");
    printf("     Social Network (C Version)\n");
    printf("==================================\n");
    printf("1. Add New User/Friendship\n");
    printf("2. Show Network\n");
    printf("3. Suggest Mutual Friends\n");
    printf("4. Find Shortest Connection\n");
    printf("5. Exit\n");
    printf("Enter choice: ");
}

// ---------------- Main ----------------
int main(int argc, char *argv[]) {
    // If run with args, handle non-interactive actions
    if (argc > 1) {
        if (strcmp(argv[1], "--init") == 0) {
            initialize_network();
            save_network_to_file(DATA_FILE);
            return 0;
        } else if (strcmp(argv[1], "--add") == 0 && argc >= 4) {
            add_user_or_friendship_noninteractive(argv[2], argv[3]);
            return 0;
        } else if (strcmp(argv[1], "--show") == 0) {
            load_network_from_file(DATA_FILE);
            show_network();
            return 0;
        } else {
            printf("Unknown arguments.\n");
            return 1;
        }
    }

    // Interactive mode (original menu)
    int choice;
    load_network_from_file(DATA_FILE);

    do {
        display_menu();
        if (scanf("%d", &choice) != 1) { while (getchar() != '\n'); choice = 0; }

        switch (choice) {
            case 1: add_user_or_friendship_interactive(); break;
            case 2: show_network(); break;
            case 3: suggest_mutual_friends(); break;
            case 4: find_shortest_connection(); break;
            case 5:
                printf("Saving network and exiting...\n");
                save_network_to_file(DATA_FILE);
                break;
            default:
                printf("Invalid choice.\n");
        }
    } while (choice != 5);

    return 0;
}