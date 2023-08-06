Advanced Usage
==============

Database Migrations
-------------------

By default, Historical models live in the same app as the model they
track. Historical models are tracked by migrations in the same way as
any other model. Whenever the original model changes, the historical
model will change also.

Therefore tracking historical models with migrations should work
automatically.


Locating past model instance
----------------------------

Two extra methods are provided for locating previous models instances on
historical record model managers.

as_of
~~~~~

This method will return an instance of the model as it would have existed at
the provided date and time.

.. code-block:: pycon

    >>> from datetime import datetime
    >>> poll.history.as_of(datetime(2010, 10, 25, 18, 4, 0))
    <Poll: Poll object as of 2010-10-25 18:03:29.855689>
    >>> poll.history.as_of(datetime(2010, 10, 25, 18, 5, 0))
    <Poll: Poll object as of 2010-10-25 18:04:13.814128>

most_recent
~~~~~~~~~~~

This method will return the most recent copy of the model available in the
model history.

.. code-block:: pycon

    >>> from datetime import datetime
    >>> poll.history.most_recent()
    <Poll: Poll object as of 2010-10-25 18:04:13.814128>


.. _register:

History for a Third-Party Model
-------------------------------

To track history for a model you didn't create, use the
``simple_history.register`` utility.  You can use this to track models from
third-party apps you don't have control over.  Here's an example of using
``simple_history.register`` to history-track the ``User`` model from the
``django.contrib.auth`` app:

.. code-block:: python

    from simple_history import register
    from django.contrib.auth.models import User

    register(User)

If you want to separate the migrations of the historical model from those of
the third-party model itself you can pass a module as ``app`` attribute to
``register``. For instance, if the migrations shall live in the migrations
folder of the package you register the model in, you could do:

.. code-block:: python

    register(User, app=__package__)

You can pass attributes of ``HistoricalRecords`` directly to ``register``:

.. code-block:: python

    register(User, excluded_fields=['last_login']))

For a complete list of the attributes you can pass to ``register`` we refer
to the source code.

Allow tracking to be inherited
---------------------------------

By default history tracking is only added for the model that is passed
to ``register()`` or has the ``HistoricalRecords`` descriptor. By
passing ``inherit=True`` to either way of registering you can change
that behavior so that any child model inheriting from it will have
historical tracking as well. Be careful though, in cases where a model
can be tracked more than once, ``MultipleRegistrationsError`` will be
raised.

.. code-block:: python

    from django.contrib.auth.models import User
    from django.db import models
    from simple_history import register
    from simple_history.models import HistoricalRecords

    # register() example
    register(User, inherit=True)

    # HistoricalRecords example
    class Poll(models.Model):
        history = HistoricalRecords(inherit=True)

Both ``User`` and ``Poll`` in the example above will cause any model
inheriting from them to have historical tracking as well.


.. recording_user:

Recording Which User Changed a Model
------------------------------------
There are three documented ways to attach users to a tracked change:

1. Use the middleware as described in :doc:`/usage`. The middleware sets the
User instance that made the request as the ``history_user`` on the history
table.

2. Use ``simple_history.admin.SimpleHistoryAdmin``. Under the hood,
``SimpleHistoryAdmin`` actually sets the ``_history_user`` on the object to
attach the user to the tracked change by overriding the `save_model` method.

3. Assign a user to the ``_history_user`` attribute of the object as described
below:

Using ``_history_user`` to Record Which User Changed a Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To denote which user changed a model, assign a ``_history_user`` attribute on
your model.

For example if you have a ``changed_by`` field on your model that records which
user last changed the model, you could create a ``_history_user`` property
referencing the ``changed_by`` field:

.. code-block:: python

    from django.db import models
    from simple_history.models import HistoricalRecords

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        changed_by = models.ForeignKey('auth.User')
        history = HistoricalRecords()

        @property
        def _history_user(self):
            return self.changed_by

        @_history_user.setter
        def _history_user(self, value):
            self.changed_by = value

Admin integration requires that you use a ``_history_user.setter`` attribute with
your custom ``_history_user`` property (see :ref:`admin_integration`).

Another option for identifying the change user is by providing a function via ``get_user``.
If provided it will be called everytime that the ``history_user`` needs to be
identified with the following key word arguments:

* ``instance``:  The current instance being modified
* ``request``:  If using the middleware the current request object will be provided if they are authenticated.

This is very helpful when using ``register``:

.. code-block:: python

    from django.db import models
    from simple_history.models import HistoricalRecords

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        changed_by = models.ForeignKey('auth.User')


    def get_poll_user(instance, **kwargs):
        return instance.changed_by

    register(Poll, get_user=get_poll_user)


Change User Model
------------------------------------

If you need to use a different user model then ``settings.AUTH_USER_MODEL``,
pass in the required model to ``user_model``.  Doing this requires ``_history_user``
or ``get_user`` is provided as detailed above.

.. code-block:: python

    from django.db import models
    from simple_history.models import HistoricalRecords

    class PollUser(models.Model):
        user_id = models.ForeignKey('auth.User')


    # Only PollUsers should be modifying a Poll
    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        changed_by = models.ForeignKey(PollUser)
        history = HistoricalRecords(user_model=PollUser)

        @property
        def _history_user(self):
            return self.changed_by

        @_history_user.setter
        def _history_user(self, value):
            self.changed_by = value

Custom ``history_id``
---------------------

By default, the historical table of a model will use an ``AutoField`` for the table's
``history_id`` (the history table's primary key). However, you can specify a different
type of field for ``history_id`` by passing a different field to ``history_id_field``
parameter.

A common use case for this would be to use a ``UUIDField``.  If you want to use a ``UUIDField``
as the default for all classes set ``SIMPLE_HISTORY_HISTORY_ID_USE_UUID=True`` in the settings.
This setting can still be overridden using the ``history_id_field`` parameter on a per model basis.

You can use the ``history_id_field`` parameter with both ``HistoricalRecords()`` or
``register()`` to change this behavior.

Note: regardless of what field type you specify as your history_id field, that field will
automatically set ``primary_key=True`` and ``editable=False``.

.. code-block:: python

    import uuid
    from django.db import models
    from simple_history.models import HistoricalRecords

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        history = HistoricalRecords(
            history_id_field=models.UUIDField(default=uuid.uuid4)
        )


Custom ``history_date``
-----------------------

You're able to set a custom ``history_date`` attribute for the historical
record, by defining the property ``_history_date`` in your model. That's
helpful if you want to add versions to your model, which happened before the
current model version, e.g. when batch importing historical data. The content
of the property ``_history_date`` has to be a datetime-object, but setting the
value of the property to a ``DateTimeField``, which is already defined in the
model, will work too.

.. code-block:: python

    from django.db import models
    from simple_history.models import HistoricalRecords

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        changed_by = models.ForeignKey('auth.User')
        history = HistoricalRecords()
        __history_date = None

        @property
        def _history_date(self):
            return self.__history_date

        @_history_date.setter
        def _history_date(self, value):
            self.__history_date = value

.. code-block:: python

    from datetime import datetime
    from models import Poll

    my_poll = Poll(question="what's up?")
    my_poll._history_date = datetime.now()
    my_poll.save()


Change Base Class of HistoricalRecord Models
--------------------------------------------

To change the auto-generated HistoricalRecord models base class from
``models.Model``, pass in the abstract class in a list to ``bases``.

.. code-block:: python

    class RoutableModel(models.Model):
        class Meta:
            abstract = True


    class Poll(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        changed_by = models.ForeignKey('auth.User')
        history = HistoricalRecords(bases=[RoutableModel])

Custom history table name
-------------------------

By default, the table name for historical models follow the Django convention
and just add ``historical`` before model name. For instance, if your application
name is ``polls`` and your model name ``Question``, then the table name will be
``polls_historicalquestion``.

You can use the ``table_name`` parameter with both ``HistoricalRecords()`` or
``register()`` to change this behavior.

.. code-block:: python

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')
        history = HistoricalRecords(table_name='polls_question_history')

.. code-block:: python

    class Question(models.Model):
        question_text = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

    register(Question, table_name='polls_question_history')

Choosing fields to not be stored
--------------------------------

It is possible to use the parameter ``excluded_fields`` to choose which fields
will be stored on every create/update/delete.

For example, if you have the model:

.. code-block:: python

    class PollWithExcludeFields(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

And you don't want to store the changes for the field ``pub_date``, it is necessary to update the model to:

.. code-block:: python

    class PollWithExcludeFields(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

        history = HistoricalRecords(excluded_fields=['pub_date'])

By default, django-simple-history stores the changes for all fields in the model.

Adding additional fields to historical models
---------------------------------------------

Sometimes it is useful to be able to add additional fields to historical models that do not exist on the
source model. This is possible by combining the ``bases`` functionality with the ``pre_create_historical_record`` signal.

.. code-block:: python

    # in models.py
    class IPAddressHistoricalModel(models.Model):
        """
        Abstract model for history models tracking the IP address.
        """
        ip_address = models.GenericIPAddressField(_('IP address'))

        class Meta:
            abstract = True


    class PollWithExtraFields(models.Model):
        question = models.CharField(max_length=200)
        pub_date = models.DateTimeField('date published')

        history = HistoricalRecords(bases=[IPAddressHistoricalModel,]


.. code-block:: python

    # define your signal handler/callback anywhere outside of models.py
    def add_history_ip_address(sender, **kwargs):
        history_instance = kwargs['history_instance']
        # thread.request for use only when the simple_history middleware is on and enabled
        history_instance.ip_address = HistoricalRecords.thread.request.META['REMOTE_ADDR']


.. code-block:: python

    # in apps.py
    class TestsConfig(AppConfig):
        def ready(self):
            from simple_history.tests.models \
                import HistoricalPollWithExtraFields

            pre_create_historical_record.connect(
                add_history_ip_address,
                sender=HistoricalPollWithExtraFields
            )


Change Reason
-------------

Change reason is a message to explain why the change was made in the instance. It is stored in the
field ``history_change_reason`` and its default value is ``None``.

By default, the django-simple-history gets the change reason in the field ``changeReason`` of the instance. Also, is possible to pass
the ``changeReason`` explicitly. For this, after a save or delete in an instance, is necessary call the
function ``utils.update_change_reason``. The first argument of this function is the instance and the second
is the message that represents the change reason.

For instance, for the model:

.. code-block:: python

    from django.db import models
    from simple_history.models import HistoricalRecords

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        history = HistoricalRecords()

You can create a instance with a implicity change reason.

.. code-block:: python

    poll = Poll(question='Question 1')
    poll.changeReason = 'Add a question'
    poll.save()

Or you can pass the change reason explicitly:

.. code-block:: python

    from simple_history.utils import update_change_reason

    poll = Poll(question='Question 1')
    poll.save()
    update_change_reason(poll, 'Add a question')

Save without a historical record
--------------------------------

If you want to save a model without a historical record, you can use the following:

.. code-block:: python

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        history = HistoricalRecords()

        def save_without_historical_record(self, *args, **kwargs):
            self.skip_history_when_saving = True
            try:
                ret = self.save(*args, **kwargs)
            finally:
                del self.skip_history_when_saving
            return ret


    poll = Poll(question='something')
    poll.save_without_historical_record()

Deleting historical record
--------------------------

In some circumstances you may want to delete all the historical records when the master record is deleted.  This can
be accomplished by setting ``cascade_delete_history=True``.

.. code-block:: python

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        history = HistoricalRecords(cascade_delete_history=True)


History Diffing
-------------------

When you have two instances of the same ``HistoricalRecord`` (such as the ``HistoricalPoll`` example above),
you can perform diffs to see what changed. This will result in a ``ModelDelta`` containing the following properties:

1. A list with each field changed between the two historical records
2. A list with the names of all fields that incurred changes from one record to the other
3. the old and new records.

This may be useful when you want to construct timelines and need to get only the model modifications.

.. code-block:: python

    p = Poll.objects.create(question="what's up?")
    p.question = "what's up, man?"
    p.save()

    new_record, old_record = p.history.all()
    delta = new_record.diff_against(old_record)
    for change in delta.changes:
        print("{} changed from {} to {}".format(change.field, change.old, change.new))

Using signals
------------------------------------
`django-simple-history` includes signals that help you provide custom behavior when saving a historical record. Arguments passed to the signals include the following:

instance
    The source model instance being saved
history_instance
    The corresponding history record
history_date
    Datetime of the history record's creation
history_change_reason
    Freetext description of the reason for the change
history_user
    The user that instigated the change

To connect the signals to your callbacks, you can use the @receiver decorator:

.. code-block:: python

    from django.dispatch import receiver
    from simple_history.signals import (
        pre_create_historical_record,
        post_create_historical_record
    )

    @receiver(pre_create_historical_record)
    def pre_create_historical_record_callback(sender, **kwargs):
        print("Sent before saving historical record")

    @receiver(post_create_historical_record)
    def post_create_historical_record_callback(sender, **kwargs):
        print("Sent after saving historical record")

History Model In Different App
------------------------------

By default the app_label for the history model is the same as the base model.
In some circumstances you may want to have the history models belong in a different app.
This will support creating history models in a different database to the base model using
database routing functionality based on app_label.
To configure history models in a different app, add this to the HistoricalRecords instantiation
or the record invocation: ``app="SomeAppName"``.

.. code-block:: python

    class Poll(models.Model):
        question = models.CharField(max_length=200)
        history = HistoricalRecords(app="SomeAppName")

    class Opinion(models.Model):
        opinion = models.CharField(max_length=2000)

    register(Opinion, app="SomeAppName")
