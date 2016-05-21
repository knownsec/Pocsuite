# Hello, World!

Thanks for your interest in making **Pocsuite** -- and therefore, the
world -- a better place!

Are you about to report a bug? Sorry to hear it. Here's our [Issue tracker].
Please try to be as specific as you can about your problem; include steps
to reproduce (cut and paste from your console output if it's helpful) and
what you were expecting to happen.

Are you about to contribute some new functionality, a bug fix, or a new
Pocsuite module? If so, read on...

# Contributing to Pocsuite

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork [the repository](https://github.com/knownsec/Pocsuite) on GitHub to start making your changes to the **dev** branch (or branch off of it).
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and bug the maintainer until it gets merged and published. Make sure to add yourself to [THANKS](./docs/THANKS.md).

## Code Contributions

* **Do** stick to the [Google Python style guide](https://google.github.io/styleguide/pyguide.html) and [Code Style](http://docs.python-guide.org/en/latest/writing/style/).
* **Do** get [Pep8](https://www.python.org/dev/peps/pep-0008/) and [Pep257](https://www.python.org/dev/peps/pep-0257/) relatively quiet against the code you are adding or modifying.
* **Do** follow the [50/72 rule] for Git commit messages.
* **Don't** use the default merge messages when merging from other branches.
* **Do** create a [topic branch] to work on instead of working directly on `master`.

### Pull Requests

* **Do** target your pull request to the **dev branch**. Not staging, not master, not release.
* **Do** specify a descriptive title to make searching for your pull request easier.
* **Do** include [console output], especially for witnessable effects in `msfconsole`.
* **Do** list [verification steps] so your code is testable.
* **Don't** leave your pull request description blank.
* **Don't** abandon your pull request. Being responsive helps us land your code faster.



#### New Modules

* **Do** run `pep8` against your module and fix any errors or warnings that come up.
* **Do** use the many module mixin [API]s. Wheel improvements are welcome; wheel reinventions, not so much.
* **Don't** include more than one module per pull request.

#### Scripts

* **Don't** submit new [scripts].  Scripts are shipped as examples for
  automating local tasks, and anything "serious" can be done with post
  modules and local exploits.

#### Library Code

* **Do** write tests - even the smallest change in library land can thoroughly screw things up.
* **Do** write **Sphinx** documentation - this makes it easier for people to use your code.
* **Don't** fix a lot of things in one pull request. Small fixes are easier to validate.

#### Bug Fixes

* **Do** include reproduction steps in the form of verification steps.
* **Do** include a link to any corresponding [Issues] in the format of
  `See #1234` in your commit description.

## Bug Reports

* **Do** write a detailed description of your bug and use a descriptive title.
* **Do** include reproduction steps, stack traces, and anything else that might help us verify and fix your bug.
* **Don't** file duplicate reports; search for your bug before filing a new report.


Also, **thank you** for taking the few moments to read this far! You're
already way ahead of the curve, so keep it up!
