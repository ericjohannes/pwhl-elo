export const pubDateString = (datetime) => {
    const pubDate =  new Date(datetime)
    console.log('datetime')
    console.log(datetime)
    console.log(pubDate)
    const months = ['Jan.','Feb.','Mar.','April','May','June','July','Aug.','Sept.','Oct.','Nov.','Dec.'];
    const year = pubDate.getFullYear();
    const month = months[pubDate.getMonth()];
    const date = pubDate.getDate();
    return month + ' ' + date + ' ' + year;
}

export const convertAndCapitalize = (str) => {
    // Replace underscores with spaces and split the string into words
    return str
      .replace(/_/g, ' ')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) // Capitalize each word
      .join(' '); // Join the words back together with spaces
}

export const roundProjection = (num) => {
    return (num*100).toFixed(0);
}