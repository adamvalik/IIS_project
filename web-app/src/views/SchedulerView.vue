<template>

  <div class="container mx-auto px-4 py-6 h-screen relative" @click="showPopup=false">

    <NavigationBar />

    <div class="py-10 px-20">
      <div class="text-center font-bold mb-4">
        Selected Animal: {{ selectedAnimal ? selectedAnimal.name : '' }}
      </div>
      <div class="flex justify-between items-center mb-4">
        <button @click="previousWeek" class="px-3 py-2 bg-gray-300 hover:bg-gray-400 rounded">&#9664;</button>
        <div class="text-center font-bold">
          Week {{ currentWeek.week }}: {{ currentWeek.startDay }}.{{ currentWeek.startMonth }}. - {{ currentWeek.endDay }}.{{ currentWeek.endMonth }}. {{ currentWeek.year }}
        </div>
        <button @click="nextWeek" class="px-3 py-2 bg-gray-300 hover:bg-gray-400 rounded">&#9654;</button>
      </div>
<!--      A grid of slots-->
      <div class="grid grid-cols-14 gap-2">
        <div></div>
        <div v-for="time in times" :key="time" class="text-center font-bold">{{ time }}</div>
        <div v-for="day in days" :key="day" class="contents">
          <div class="text-right font-bold pr-2">{{ day }}</div>
          <div v-for="time in times" :key="day + time"
               :class="getClass(getSlot(day, time))"
               @click.stop ="toggleSelection(day, time)"
               class="border p-2 cursor-pointer relative">
          </div>
        </div>
      </div>

      <!-- Legend -->
      <div class="mt-7 mb-4">
        <div v-if="getRole === 'volunteer'" class="flex justify-around flex-col md:flex-row">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-400 mr-2"></div>
            <span>Approved</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-red-400 mr-2"></div>
            <span>Reserved</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-blue-400 mr-2"></div>
            <span>Available</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-orange-400 mr-2"></div>
            <span>Pending</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-yellow-400 mr-2"></div>
            <span>Selected</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-gray-200 mr-2"></div>
            <span>Unavailable</span>
          </div>
        </div>
        <div v-else class="flex justify-around flex-col md:flex-row">
          <div class="flex items-center">
            <div class="w-4 h-4 bg-green-400 mr-2"></div>
            <span>Approved</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-blue-400 mr-2"></div>
            <span>Available</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-orange-400 mr-2"></div>
            <span>Pending</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-pink-400 mr-2"></div>
            <span>New Slot</span>
          </div>
          <div class="flex items-center">
            <div class="w-4 h-4 bg-gray-200 mr-2"></div>
            <span>Unavailable</span>
          </div>
        </div>
      </div>
<!--      Logic for the buttons which either appear or disappear based on the user's role:-->
      <button v-if="getRole !== 'caregiver'" class="mt-5 py-2 px-3 rounded-lg font-semibold bg-green-500 hover:bg-green-600 text-white" @click="confirmSelection">
        Confirm Reservation
      </button>

      <button v-if="getRole === 'caregiver'" class="mt-5 py-2 px-3 rounded-lg font-semibold bg-green-500 hover:bg-green-600 text-white" @click="createNewSlot">
        Create New Slots
      </button>

      <!-- Pop-up Window -->
      <div v-if="showPopup.visible" class="popup absolute bg-white border p-4 rounded shadow-lg" style="top: 30%; left: 50%; transform: translate(-50%, -50%); z-index: 50;" @click.stop>
        <p class="font-bold">{{ approvalText }}</p>
        <p v-if="getRole === 'caregiver'">
          Name:
          <router-link :to="`/user/${showPopup.user_id}`" class="text-blue-500 hover:text-blue-600">
            {{ userReserve }}
          </router-link>
        </p>
        <p>Time: {{ showPopup.time }}</p>
        <p>Date: {{ showPopup.date }}</p>
        <div class="flex justify-evenly mt-2" :class="getRole === 'caregiver' ? 'gap-16' : ''">
          <button @click="cancelReservation" class="mt-2 px-3 py-1 bg-red-500 hover:bg-red-600 text-white rounded-md font-semibold">Cancel Reservation</button>
          <button v-if="getRole === 'caregiver'" @click="approveReservation" class="mt-2 px-3 py-1 bg-green-500 hover:bg-green-600 text-white rounded-md font-semibold">Approve Reservation</button>
        </div>
        <p v-if="getRole === 'volunteer'" class="text-sm text-gray-500 mt-2">If you are canceling less than 24 hours before the appointment, please call us at +123456789</p>
      </div>

    </div>
  </div>
</template>

<script>
import apiClient from '@/api';
import NavigationBar from '@/components/NavigationBar.vue';
import axios from 'axios';
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'userRole', 'tokenExp', 'user_id']),
    getID() {
      return this.user_id;
    },
    getRole() {
      return this.userRole;
    },
    approvalText() {
      return this.isApproved ? 'Approved Reservation' : 'Waiting for approval';
    },
    userReserve() {
      return this.userReservation;
    }
  },
  components: {
    NavigationBar
  },
  watch: {
    'showPopup.visible'(newVal) {
      if (newVal) {
        this.checkApprovalStatus();
      }
    }
  },
  name: 'SchedulerView',
  data() {
    return {
      // Data for the scheduler
      currentDate: new Date(),
      currentWeek: {},
      selectedAnimal: {name: ''},
      // Static data for days and times
      days: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
      times: ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00'],
      schedule: [],
      selected: [],
      new_slots: [],
      // Slot popup
      hoveredSlot: {day: null, time: null},
      showPopup: { visible: false, day: '', time: '', date: '', user_id: '' },
      isApproved: false,
      userReservation: '',
      animal_id: null
    };
  },
  created() {
    axios.defaults.headers.common['Authorization'] = `Bearer ${this.$store.state.accessToken}`;
    this.currentWeek = this.getWeekDetails(this.currentDate);
    this.animal_id = this.$route.params.id;
    this.fetchName(this.animal_id);
    this.fetchSchedule(); // Fetch the schedule and name of the now-viewed animal when component is created
  },
  methods: {
    getWeekDetails(date) {
      const currentDate = new Date(date);
      let dayOfWeek = currentDate.getDay();
      if (dayOfWeek === 0) dayOfWeek = 7; // Convert Sunday from 0 to 7 to handle week start correctly
      const startOfWeek = new Date(currentDate);
      startOfWeek.setDate(currentDate.getDate() - dayOfWeek + 1); // Set to Monday of the current week (by default it is Sunday)

      const endOfWeek = new Date(startOfWeek);
      endOfWeek.setDate(startOfWeek.getDate() + 6);

      // Extract month and year
      const startMonth = startOfWeek.getMonth() + 1;
      const endMonth = endOfWeek.getMonth() + 1;
      const startDay = startOfWeek.getDate();
      const endDay = endOfWeek.getDate();
      const year = currentDate.getFullYear();

      return {
        // Calculate the week number 604800000 = 7 * 24 * 60 * 60 * 1000
        week: Math.ceil((currentDate - new Date(currentDate.getFullYear(), 0, 1)) / 604800000),
        startMonth: startMonth,
        endMonth: endMonth,
        startDay: startDay,
        endDay: endDay,
        year: year
      };
    },
    fetchName(id) {
      apiClient.get(`/animals/animal_name/${id}`)
        .then(response => {
          this.selectedAnimal.name = response.data;
        })
        .catch(error => {
          console.error('Error fetching animal:', error);
        });
    },
    fetchSchedule() {

      const currentDate = new Date(this.currentDate);
      const dayOfWeek = currentDate.getDay();
      const startOfWeek = new Date(currentDate.setDate(currentDate.getDate() - (dayOfWeek === 0 ? 6 : dayOfWeek - 1)));
      const startDate = startOfWeek.toISOString().split('T')[0];
      const animal_id = this.animal_id;
      const user_id = this.getID;

      apiClient.post('/schedule', {
        user_id: user_id,
        animal_id: animal_id,
        date: startDate
      })
        .then(response => {
          const scheduleData = response.data.schedule;
          this.schedule = Array.from({ length: 7 }, (_, day) =>
            Array.from({ length: 13 }, (_, hour) =>
              scheduleData[day]?.[hour + 9] || "blue" // Map backend data to array format
            )
          );
        })
        .catch(error => {
          console.error('Error fetching schedule:', error);
        });
    },
    getSlot(day, time) {
      const dayIndex = this.days.indexOf(day);
      const timeIndex = parseInt(time.split(':')[0]) - 9; // convert time string (e.g., "09:00") to an hour offset

      if (
          dayIndex >= 0 && dayIndex < 7 &&
          this.schedule[dayIndex] &&
          this.schedule[dayIndex][timeIndex] !== undefined
      ) {
        return this.schedule[dayIndex][timeIndex];
      }
      return 'gray';
    },
    getClass(slot) {
      if (slot === 'green') return 'bg-green-400 hover:bg-green-500';
      if (slot === 'red') return 'bg-red-400 hover:bg-red-500';
      if (slot === 'blue') return 'bg-blue-400 hover:bg-blue-500';
      if (slot === 'orange') return 'bg-orange-400 hover:bg-orange-500';
      if (slot === 'pink') return 'bg-pink-400 hover:bg-pink-500';
      if (slot === 'selected') return 'bg-yellow-400 hover:bg-yellow-500';
      return 'bg-gray-200 hover:bg-gray-300';
    },
    // Logic (if - else constructions) for the buttons which either appear or disappear based on the user's role
    toggleSelection(day, time) {
      const dayIndex = this.days.indexOf(day);
      const timeIndex = this.times.indexOf(time);

      if (dayIndex >= 0 && timeIndex >= 0) {
        const startOfWeek = new Date(this.currentDate);
        let dayOfWeek = startOfWeek.getDay();
        if (dayOfWeek === 0) dayOfWeek = 7; // Adjust for Sunday being 0
        startOfWeek.setDate(startOfWeek.getDate() - dayOfWeek + 1);

        const selectedDate = new Date(startOfWeek);
        selectedDate.setDate(startOfWeek.getDate() + dayIndex);
        const formattedDate = selectedDate.toISOString().split('T')[0];

        // Check if the selected date and time are older than the current date and time
        const currentDate = new Date();
        const selectedDateTime = new Date(`${formattedDate}T${time}:00`);
        if (selectedDateTime < currentDate) {
          return;
        }

        const slotStatus = this.getSlot(day, time);
        if (slotStatus === 'green' || slotStatus === 'orange') {
          this.showPopup = { visible: true, day, time, date: formattedDate };
        } else {
          if (this.showPopup.visible) {
            this.showPopup.visible = false;
          }
        }

        if (slotStatus === 'blue' && this.getRole !== 'caregiver') {
          this.schedule[dayIndex][timeIndex] = 'selected';
          this.selected.push({ day, time });
        } else if (slotStatus === 'selected') {
          this.schedule[dayIndex][timeIndex] = 'blue';
          this.selected = this.selected.filter(s => !(s.day === day && s.time === time));
        } else if (slotStatus === 'blue' && this.getRole === 'caregiver') {
          this.deleteSlot(day, time);
        } else if (slotStatus === 'gray' && this.getRole === 'caregiver') {
          this.new_slots.push({ day, time });
          this.schedule[dayIndex][timeIndex] = 'pink';
        } else if (slotStatus === 'pink' && this.getRole === 'caregiver') {
          this.schedule[dayIndex][timeIndex] = 'gray';
          this.new_slots = this.new_slots.filter(s => !(s.day === day && s.time === time));
        }
      }
    },
    createNewSlot() {
      const startOfWeek = new Date(this.currentDate);
      let dayOfWeek = startOfWeek.getDay();
      if (dayOfWeek === 0) dayOfWeek = 7; // Adjust for Sunday being 0
      startOfWeek.setDate(startOfWeek.getDate() - dayOfWeek + 1);

      const newSlots = this.new_slots.map(slot => {
        const dayIndex = this.days.indexOf(slot.day);
        const selectedDate = new Date(startOfWeek);
        selectedDate.setDate(startOfWeek.getDate() + dayIndex);
        const formattedDate = selectedDate.toISOString().split('T')[0];
        return { day: slot.day, time: slot.time, date: formattedDate };
      });
      const animal_id = this.animal_id;
      apiClient.post('/createslot', {
        animal_id: animal_id,
        new_slots: newSlots
      })
        .then(response => {
          newSlots.forEach(slot => {
            const dayIndex = this.days.indexOf(slot.day);
            const timeIndex = this.times.indexOf(slot.time);
            this.schedule[dayIndex][timeIndex] = 'blue';
          });
          this.new_slots = []; // Clear the new slots
        })
        .catch(error => {
          console.error('Error creating slot:', error);
        });
    },
    confirmSelection() {
      const startOfWeek = new Date(this.currentDate);
      let dayOfWeek = startOfWeek.getDay();
      if (dayOfWeek === 0) dayOfWeek = 7; // Adjust for Sunday being 0
      startOfWeek.setDate(startOfWeek.getDate() - dayOfWeek + 1);

      const selectedSlots = this.selected.map(slot => {
        const dayIndex = this.days.indexOf(slot.day);
        const selectedDate = new Date(startOfWeek);
        selectedDate.setDate(startOfWeek.getDate() + dayIndex);
        const formattedDate = selectedDate.toISOString().split('T')[0];
        return { day: slot.day, time: slot.time, date: formattedDate };
      });
      const user_id = this.getID;
      apiClient.post('/confirmselection', {
        user_id: user_id,
        animal_id: this.animal_id,
        slots: selectedSlots
      })
          .then(response => {
            // Make the slots orange to indicate pending confirmation
            selectedSlots.forEach(slot => {
              const dayIndex = this.days.indexOf(slot.day);
              const timeIndex = this.times.indexOf(slot.time);
              this.schedule[dayIndex][timeIndex] = 'orange';
            });
            this.selected = []; // Clear the selected slots
          })
          .catch(error => {
            console.error('Error confirming reservation:', error);
          });
    },
    previousWeek() {
      this.currentDate.setDate(this.currentDate.getDate() - 7);
      this.currentWeek = this.getWeekDetails(this.currentDate);
      this.fetchSchedule(); // Fetch new week data
    },
    nextWeek() {
      if (this.new_slots.length > 0) {
        alert('Please save or cancel the new slots before proceeding to the next week.');
        return;
      }
      this.currentDate.setDate(this.currentDate.getDate() + 7);
      this.currentWeek = this.getWeekDetails(this.currentDate);
      this.fetchSchedule(); // Fetch new week data
    },
    cancelReservation() {
      const { day, time, date } = this.showPopup;
      const dayIndex = this.days.indexOf(day);
      const timeIndex = this.times.indexOf(time);

      if (dayIndex >= 0 && timeIndex >= 0) {
        this.showPopup.visible = false;
        const reservationDate = new Date(date);
        const currentDate = new Date();

        // Check if the reservation date is in the past
        if (reservationDate < currentDate) {
          alert('Cannot cancel reservations for past dates.');
          return;
        }

        const animalId = this.animal_id;
        const userId = this.getID;
        apiClient.delete(`/cancel/${userId}/${animalId}/${date}/${time}`)
            .then(response => {
              this.schedule[dayIndex][timeIndex] = 'blue';
              this.selected = this.selected.filter(s => !(s.day === day && s.time === time));
            })
            .catch(error => {
              console.error('Error canceling reservation:', error);
            });
      }
    },
    deleteSlot(day, time) {
      const dayIndex = this.days.indexOf(day);
      const timeIndex = this.times.indexOf(time);

      const startOfWeek = new Date(this.currentDate);
      let dayOfWeek = startOfWeek.getDay();
      if (dayOfWeek === 0) dayOfWeek = 7; // Adjust for Sunday being 0
      startOfWeek.setDate(startOfWeek.getDate() - dayOfWeek + 1);

      const selectedDate = new Date(startOfWeek);
      selectedDate.setDate(startOfWeek.getDate() + dayIndex);
      const formattedDate = selectedDate.toISOString().split('T')[0];

      if (dayIndex >= 0 && timeIndex >= 0) {

        const animalId = this.animal_id;
        apiClient.delete(`/delete/${animalId}/${formattedDate}/${time}`)
          .then(response => {
            this.new_slots = this.new_slots.filter(s => !(s.day === day && s.time === time));
            this.schedule[dayIndex][timeIndex] = 'gray';
          })
          .catch(error => {
            console.error('Error deleting slot:', error);
          });
      }
    },
    approveReservation(){
      const { day, time, date } = this.showPopup;
      const dayIndex = this.days.indexOf(day);
      const timeIndex = this.times.indexOf(time);

      if (dayIndex >= 0 && timeIndex >= 0) {
        this.schedule[dayIndex][timeIndex] = 'green';
        this.showPopup.visible = false;

        const animalId = this.animal_id;
        apiClient.post('/approve/', {
          animal_id: animalId,
          date: date,
          time: time
        })
        .catch(error => {
          console.error('Error approving reservation:', error);
        });
      }
    },
    async checkApprovalStatus() {
      const animal_id = this.animal_id;
      // Check if the selected slot is approved
      try {
        const response = await apiClient.get(`/checkApproval/${animal_id}/${this.showPopup.date}/${this.showPopup.time}`);
        this.isApproved = response.data.isApproved;
        this.userReservation = response.data.username;
        this.showPopup.user_id = response.data.user_id;
      } catch (error) {
        console.error('Error checking approval status:', error);
      }
    },
  }
};
</script>

<style scoped>
.schedule-container {
  max-width: 900px;
  margin: 0 auto;
}

.grid-cols-14 {
  grid-template-columns: repeat(14, 1fr);
}

.border {
  border: 1px solid #ddd;
}

.info-table {
  top: 0;
  left: 100%;
  z-index: 10;
  width: 150px;
  transform: translateX(10px);
}
</style>
