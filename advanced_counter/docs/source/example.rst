Example Implementations
=======================

Below is a simple example application using NamedCounter and AdvCounter

.. code-block:: python

    from advanced_counter import NamedCounter, AdvCounter


    def print_status(counter)
        print('Completed %s records' % counter.all.prec_str)

    def import_rental_records(records, existing_records):
        """
        Imports a list of records for store front rental properties, also allows properties to be removed from the list.

        Imports dict records with keys of:
            'rental_id': a unique field identifying the property,
            'monthly_rent': a value of the total rent due per month
            'size': a string 'large', 'med', 'small' identifying the store front size.
            'delete': if 'yes', this property will be deleted from the list.

        """
        # here we create the total_records counter, we need to do this
        # seperatly since we are adding the call_every function)

        all_counter = AdvCounter(
            max_counter=len(records),
            min_counter=1,
            call_every='10%',
            call_every_func=print_status)

        # Here we create the NamedCounter object, we are creating counters for the various things that we want to track
        # Note the "total_space" counter, since the records dont have the number of sq_ft in the store, we are using a
            IncrementByDict helper to add that number.  (yes, we could have simply looked up the number and added it, but
            what's the fun in that.)

        counters = NamedCounter(
            name='Records Imported',
            total_imported={'name': 'Total Imported', value: all_counter},  # this is where we use the earlier defined counter
            created='Created/Updated Records',
            deleted='Deleted Records',
            total_space={'name':'Total Space', increment_on={'small': 500, 'med': 1000, 'large': 5000})
            total_rent='Total Rent')

        for record in records:
            # increment the total number of records imported.
            #    note this will update the screen every 10%
            counters.total_imported()

            if record['delete'] in existing_records:
                del existing_records[record['key']]

                # update the counter for the number of deleted records
                counters.deleted()

                continue
            existing_recprds[record['key'] = record

            # update the number of records added or updated
            counters.created()

            # update the total space under contract (here we are taking the string size and converting it to a number
            #    which is added to the counter
            counters.total_space.add(record['size'])

            # update the total rent that we expect to get every month.
            counters.total_rent.add(record['monthly_rent']

        # print out a list of completed counters at the end of the process.
        print()
        print(counters.report())


when running this, we would expect to see somthing like the following:

.. code-block::

    >>> import_rental_records(records, existing_records)
    Completed 10% of records
    Completed 20% of records
    Completed 30% of records
    Completed 40% of records
    Completed 50% of records
    Completed 60% of records
    Completed 70% of records
    Completed 80% of records
    Completed 90% of records
    Completed 100% of records

    Records Imported
                 Total Imported: 454
                Deleted Records: 54
        Created/Updated Records: 400
                    Total Space: 1450000
                     Total Rent: 2340332

