# Math_Bulls_Cows
https://www.youtube.com/watch?v=heaEKqW0GqQ
https://www.youtube.com/watch?v=VuoPjr4qR7M

This project uses Shannon entropy to measure how much uncertainty remains about the secret number at every turn of the game.

1. What entropy represents
At any point in the game, we maintain a set:
𝑆 = all possible secret numbers still consistent with the feedback

Entropy is: H(S)=log2∣S∣

This value tells us how many bits of uncertainty we have about the secret.
∣S∣ is large → high entropy → we know very little
∣S∣ is small → low entropy → we are close to the answer
∣S∣=1 → entropy = 0 → the secret is logically determined

Entropy is the core mathematical measurement of our knowledge.
​
2. How entropy changes after each guess

When the player makes a guess, we calculate Bulls and Cows
Then we filter the candidate set: 𝑆 ={s∈S ∣bulls_cows(s,guess)=(b,c)}

New entropy: H(S′)=log2∣S′∣
This always drops, meaning uncertainty decreases.
Entropy is printed after every guess so the player can watch their uncertainty shrink in real time.

3. How entropy helps build the best strategy
We can predict how informative each potential guess might be by calculating Expected Information Gain.​
The best guess is the one with the highest expected information gain.

4. When entropy becomes zero

Entropy becomes zero when: ∣S∣=1
This means we logically know the secret.

Entropy staying at zero is correct but uncertainty cannot go negative.
