command is run
> splits up name of poll and arguments
> message is sent
> message location is stored + name + id
> options are stored in seperate table

reaction is caught
> check if its on right message
> if it has id, check emote to get poll option id

```python

sql3 = "INSERT INTO votes (`poll_id`, `user_id`, `option_id`) VALUES (%s,%s,%s)"

try:
    self.cursor.execute(sql3, (poll_id[0][0], user_id, option_id[0][0]))
    self.conn.commit()
except  Exception as exc:
    self.conn.rollback()
    print(str(exc))
```

check if done
> select time ordered and pick earliest


furture boloptz

id in poll options is unessesary
composite key using poll id and emote "id" will handle situation
votes imports table from emote id

you bean
you need to toggle the votes on add role
