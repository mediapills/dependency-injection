Overview
========

.. warning:: This Document Page Under Construction

**Dependency Injection** is a technique in which an object receives other
objects that it depends on, called dependencies. Typically, the receiving
object is called a client and the passed-in ('injected') object is called a
service. The code that passes the service to the client is called the injector.
Instead of the client specifying which service it will use, the injector tells
the client what service to use. The 'injection' refers to the passing of a
dependency (a service) into the client that uses it.

Dependency injection solves the following problems:

- How can a class be independent of how the objects on which it depends are created?
- How can the way objects are created be specified in separate configuration files?
- How can an application support different configurations?

Creating objects directly within the class commits the class to particular
implementations. This makes it difficult to change the instantiation at
runtime, especially in compiled languages where changing the underlying objects
can require re-compiling the source code.

Dependency injection separates the creation of a client's dependencies from the
client's behavior, which promotes loosely coupled programs and the dependency
inversion and single responsibility principles. Fundamentally, dependency
injection is based on passing parameters to a method.

Dependency injection is an example of the more general concept of inversion of
control.

Roles
-----

Dependency injection involves four roles:

* the service objects to be used
* the client object, whose behavior depends on the services it uses
* the interfaces that define how the client may use the services
* the injector, which constructs the services and injects them into the client

Any object that may be used can be considered a **service**. Any object that
uses other objects can be considered a **client**. The names relate only to the
role the objects play in an injection.

The **interfaces** are the types the client expects its dependencies to be. The
client should not know the specific implementation of its dependencies, only
know the interface's name and API. As a result, the client will not need to
change even if what is behind the interface changes. Dependency injection can
work with true interfaces or abstract classes, but also concrete services,
though this would violate the dependency inversion principle and sacrifice the
dynamic decoupling that enables testing. It is only required that the client
never treats its interfaces as concrete by constructing or extending them. If
the interface is refactored from a class to an interface type (or vice versa)
the client will need to be recompiled. This is significant if the client and
services are published separately.

The **injector** introduces services to the client. Often, it also constructs
the client. An injector may connect a complex object graph by treating the same
object as both a client at one point and as a service at another. The injector
itself may actually be many objects working together, but may not be the client
(as this would create a circular dependency). The injector may be referred to
as an assembler, provider, container, factory, builder, spring, or construction
code.

Pros
----

A basic benefit of dependency injection is decreased coupling between classes
and their dependencies. By removing a client's knowledge of how its
dependencies are implemented, programs become more reusable, testable and
maintainable.

This also results in increased flexibility: a client may act on anything that
supports the intrinsic interface the client expects.

Many of dependency injection's benefits are particularly relevant to
unit-testing.

For example, dependency injection can be used to externalize a system's
configuration details into configuration files, allowing the system to be
reconfigured without recompilation. Separate configurations can be written for
different situations that require different implementations of components. This
includes testing. Similarly, because dependency injection does not require any
change in code behavior it can be applied to legacy code as a refactoring. The
result is clients that are more independent and that are easier to unit test in
isolation using stubs or mock objects that simulate other objects not under
test. This ease of testing is often the first benefit noticed when using
dependency injection.

More generally, dependency injection reduces boilerplate code, since all
dependency creation is handled by a singular component.

Finally, dependency injection allows concurrent development. Two developers can
independently develop classes that use each other, while only needing to know
the interface the classes will communicate through. Plugins are often developed
by third party shops that never even talk to the developers who created the
product that uses the plugins.

Cons
----

Creates clients that demand configuration details, which can be onerous when
obvious defaults are available.

Make code difficult to trace because it separates behavior from construction.

Is typically implemented with reflection or dynamic programming. This canhinder
IDE automation.

Typically requires more upfront development effort.

Forces complexity out of classes and into the links between classes which might
be harder to manage.

Encourage dependence on a framework.
