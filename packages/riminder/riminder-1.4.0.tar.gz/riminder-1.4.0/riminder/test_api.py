from riminder import Riminder

client = Riminder(api_key='ask_5bd45b534bd4f1625f21b9a705c0d711')

print(client)

res = client.profile.reveal.get(
            source_id='f06a369b22c76ac89f96338c44b1d578862bc6d3',
            profile_id='228268',
            filter_reference='21051996'
        )

print(res)