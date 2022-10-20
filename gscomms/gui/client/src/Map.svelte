<script lang="ts">
    import {Map, Marker} from '@beyonk/svelte-mapbox'

    async function getToken() {
        const res = await fetch('/map_token');
        const token = res.json()['token'];

        if (res.ok) {
            return token;
        } else {
            throw new Error(res.statusText);
        }
    }

    let mapComponent: any;
</script>

{#await getToken()}
    <p>Getting map token...</p>
{:then token}
    <Map accessToken={token} bind:this={mapComponent}>
        <Marker lat={40.4273} lng={86.9141} label="Purdue"/>
    </Map>
{:catch error}
    <p style="color: red">Failed to load token: {error.message}</p>
{/await}