Title: 💩2vec - Emojis in Python (1/4)
Date: 2017-01-08
Category: Blogs
Series: 💩2vec

In this three part series we'll try to find the meaning of and relation between emojis.
First, we'll look at how to process emojis in Python.
This post shows how to handle text data with all kind of different characters and then specifically to handle text with emojis.


## Unicode and Python

Character encoding systems represent a set of characters by codes.
Morse code, for example, encodes (mostly) Latin characters by dots and dashes.
Unicode is a standard that tries to encode, represent and handle almost _any_ character: it's not only limited to Latin characters, but also includes Chinese and Russian characters. 

Unicode doesn't specify how all these characters look like, it only specifies a code point to (almost) every possible character.
For example, `U+0041` is the code point for A: `U+` stands for Unicode and the integer `0041` is 65 in hexadecimal format.
Similarly, Ƃ is `U+0182`, Ɱ is `U+2C6E` and 💩 is `U+1F4A9`.
Yes, emojis are also part of Unicode! 🙌

Character encodings specify how the code points are stored as bytes in memory.
Computes don't store code points, they store bytes; encodings tell computers how to encode code points to bytes.
Unicode encodings go by names such as UTF-8 and UTF-16.
🙏, also known as 'folded hands' or `U+1F64F`, is stored as `f09f998f` in UTF-8 and `d83dde4f` in UTF-16.
You need to know what encoding was used to correctly read encoded characters.

Python has Unicode strings and byte strings. 
In Python 3 `str` is a Unicode string by default and `bytes` is a byte string.
Generally speaking, byte strings are used for storing strings in memory and  Unicode strings are used in your program.

Encode Unicode strings to get bytes: 

```{python3}
In [1]: '🙏'.encode('utf-16')
Out[1]: b'\xff\xfe=\xd8O\xde'
```

Decode bytes to get Unicode strings:

```{python3}
In [2]: b'\xff\xfe=\xd8O\xde'.decode('utf-16')
Out[2]: '🙏'
```

How should you handle Unicode and bytes in Python?
Things will generally go smooth if you decode files to Unicode when reading and use Unicode only in Python.
Encode back to bytes again when saving.
In Python 2, working with Unicode and byte strings might be a bit more complicated.

On a side note, Python 3 also Unicode support for variable *names*. This can be excellent for writing code that's a pain to read/refactor:

```{python3}
In [3]: Ɱ = 'foo'
   ...: Ɱ
Out[3]: 'foo'
```

Unfortunately, emojis are not supported yet 😥:

```{python3}
In [4]: 🙏 = 'foo'
  File "<ipython-input-2-be820f43e6fa>", line 1
    🙏 = 'foo'
    ^
SyntaxError: invalid character in identifier
```

So emojis are characters, characters are represented by code points and code points are stored as bytes.
Just get the right code points to encode the emojis and that's all there is, right?
Almost.


## Unicode and emojis

Unicode contains more than 128,000 characters and 1000 code points are emojis, meaning that around 1% of the code points are emojis!
However, the list with supported emojis is longer: there are currently 1200 emojis:

<center>
<img src="{filename}/images/emoji2vec/n_emojis.png" alt="Drawing" style="width: 500px;"/>
</center>

Looking at the [full list](http://unicode.org/emoji/charts/full-emoji-list.html) of emojis, there are many emojis that are similar and only differ by color. 
💂🏽 is a modified version of  💂 , 🎅🏿 of 🎅, and 👦🏼 of 👦.

Not all characters are encoded by a single code point, some characters are represented by multiple code points.
National flags consist of two code points:

```{python}
In [5]: flag = '🇳' + '🇱'
   ...: flag
Out[5]: '🇳🇱'
```

Some emojis change skin colour depending on the [Fitzpatrick](https://en.wikipedia.org/wiki/Fitzpatrick_scale) modifier:

```{python}
In [6]: for modifier in ['🏻', '🏼', '🏽', '🏾', '🏿']:
   ...:     print('💂' + modifier)
💂🏻
💂🏼
💂🏽
💂🏾
💂🏿
```

If we want to properly process emojis, we clearly shouldn't look at them as single code point but as _sequences_ of code points. 

How emojis look like and if you can even see them properly, depends on your platform (and the chosen [presentation style](http://www.unicode.org/emoji/charts/emoji-style.html)).
The table below shows some of the possible [variations](http://unicode.org/emoji/charts/full-emoji-list.html):

<center>

Your browser | Apple | Facebook | Google | Samsung | Twitter
:----------: | :---: | :------: | :----: | :-----: | :-----:
🐎 | <img src="{filename}/images/emoji2vec/apple_U+1F40E.png" alt="Drawing" style="width: 20px;"/> | <img src="{filename}/images/emoji2vec/facebook_messenger_U+1F40E.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/google_U+1F40E.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/samsung_U+1F40E.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/twitter_U+1F40E.png" alt="Drawing" style="width: 20px;"/>
😅 | <img src="{filename}/images/emoji2vec/apple_U+1F605.png" alt="Drawing" style="width: 20px;"/> | <img src="{filename}/images/emoji2vec/facebook_messenger_U+1F605.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/google_U+1F605.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/samsung_U+1F605.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/twitter_U+1F605.png" alt="Drawing" style="width: 20px;"/>
🐼 | <img src="{filename}/images/emoji2vec/apple_U+1F43C.png" alt="Drawing" style="width: 20px;"/> | <img src="{filename}/images/emoji2vec/facebook_messenger_U+1F43C.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/google_U+1F43C.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/samsung_U+1F43C.png" alt="Drawing" style="width: 20px;"/>| <img src="{filename}/images/emoji2vec/twitter_U+1F43C.png" alt="Drawing" style="width: 20px;"/>

</center>

## Conclusion

We now know how to use emojis in Python.
Emojis are encoded as sequences of one or multiple Unicode code points, the encoding specifies in what format the computer saves the emojis and our platform determines how emojis look like.
Up next: processing tweets!


## Related
* Joel Spolsky on [Unicode](http://www.joelonsoftware.com/articles/Unicode.html).
* Ned Batchelder on [using Unicode in Python 2 and 3](http://nedbatchelder.com/text/unipain.html).
* [Reddit thread](https://www.reddit.com/r/Python/comments/1g62eh/explain_it_like_im_five_python_and_unicode/) on Python and Unicode
* [FAQ](http://www.unicode.org/faq/emoji_dingbats.html) on Unicode emojis
