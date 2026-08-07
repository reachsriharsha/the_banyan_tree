minimal application which should have a way to add:

* the students name

* date of birth

* the address

* a parent contact number, there should be 2 contact numbers, choose between father, mother, guardian

These details for each swimmer, student name, DoB is mandatory. For Parent one will be primary and that will be mandatory.

Home page will have login | register club
login: user enters their phone number and they will get OTP delivered 
register club: will open the form, with name of club, head coach phone number, head coach name once they submit it will be stored in db and email will be sent to super admin. 
super user login where crud for the coaching club present. 

Once the users log in:
Who can add assistant coaches?: Head coach(who has registered the school)
Who can add students?: Head coach and assistant  coaches
Who can log the entries for the students swim session?: Head and assistant coach

Session details:
Daily there will be 2 session morning session evening sessison
each student attendance marked in each session. By default present
timing can be entered optional in separate page for different kind of styles of swimming.  



Since this is very niche product: I want simple tech stack below
1. fast api for backend
2. sqlite for database storage
3. each swimming academy gets its own db file
4. there will be control db which has the user details which is used for log in
5. All student info with respect to the coaching center stays in the coaching center db.
6. time  recording also present in the coaching center speciific db for each student. 

## Linked Sessions

### August 2026
- [[sessions/session-2026-08-04-15-13-b09feb68|2026-08-04 15:13]] — SwimAcademy MVP built from spec, dockerized (single `./run.sh` → docker-compose), poolside quick-entry UX, category-based demo seed (repo `cadencelanes`)
