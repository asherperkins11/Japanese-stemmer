# JapaneseStemmer
JapaneseStemmer a Japanese stemming algorithm I made for a school project, which is based on Martin Porter's Porter Stemming Algorithm. Unlike Porter's algorithm, which focuses on removing a word's ending, this stemming algorithm conjugates a word into plain form. Although the code works there is still room for improvemnt, and feedback is appreciated.

# Usage
```
stemming("Word to be stemmed")
```
This function returns the conjugated word as a string.

Instead of returning the literal word stem, JapaneseStemmer conjugates the token into plain form. So, the token 食べなかった is returned as 食べる, not 食べ.

This implementation is somewhat limited however. As word forms such as [Te](http://www.punipunijapan.com/te-form-making-requests/) or [Tai](http://www.punipunijapan.com/tai-form/) cannot be accurately conjugated without the use of a dictionary or large lookup table, I decided to leave them out for simplicity's sake.
